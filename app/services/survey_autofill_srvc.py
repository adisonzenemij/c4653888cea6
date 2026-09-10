import asyncio
import ctypes
import os
from pathlib import Path
import uuid

from fastapi import HTTPException, status
from playwright.async_api import Error as PlaywrightError, Page, async_playwright
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.models.entities_model import Pm0acc84aeModel, Pm4d802b91Model, Pm9a582ff6Model
from app.services.entity_srvcs import Pm4d802b91Service


class SurveyAutoFillService:
    """Completes survey participations through headless Chromium in this runtime."""

    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def memory_capacity(bots: int) -> dict[str, int]:
        """Return a conservative per-bot budget from host or cgroup memory."""
        available = SurveyAutoFillService._available_memory_mb()
        cgroup_available = SurveyAutoFillService._cgroup_available_memory_mb()
        if cgroup_available is not None:
            available = min(available, cgroup_available)
        # Preserve capacity for FastAPI, MySQL connections and the OS/container.
        reserved = min(256, max(1, available // 5))
        usable = max(1, available - reserved)
        return {
            "available_mb": available,
            "reserved_mb": reserved,
            "max_memory_per_bot_mb": max(1, usable // max(1, bots)),
        }

    @staticmethod
    def _available_memory_mb() -> int:
        meminfo = Path("/proc/meminfo")
        if meminfo.exists():
            values = {
                key.rstrip(":"): int(value.split()[0])
                for line in meminfo.read_text().splitlines()
                if (parts := line.split(maxsplit=1)) and len(parts) == 2
                for key, value in [parts]
                if value.split()[0].isdigit()
            }
            if values.get("MemAvailable"):
                return max(1, values["MemAvailable"] // 1024)
        if os.name == "nt":
            class MemoryStatus(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]
            status_info = MemoryStatus()
            status_info.dwLength = ctypes.sizeof(MemoryStatus)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status_info)):
                return max(1, status_info.ullAvailPhys // (1024 * 1024))
        return 512

    @staticmethod
    def _cgroup_available_memory_mb() -> int | None:
        candidates = [
            (Path("/sys/fs/cgroup/memory.max"), Path("/sys/fs/cgroup/memory.current")),
            (Path("/sys/fs/cgroup/memory/memory.limit_in_bytes"), Path("/sys/fs/cgroup/memory/memory.usage_in_bytes")),
        ]
        for limit_path, usage_path in candidates:
            if not limit_path.exists() or not usage_path.exists():
                continue
            raw_limit = limit_path.read_text().strip()
            if raw_limit == "max":
                continue
            try:
                limit = int(raw_limit)
                usage = int(usage_path.read_text().strip())
            except ValueError:
                continue
            # Very large values mean the container has no effective limit.
            if limit >= 1 << 60:
                continue
            return max(1, (limit - usage) // (1024 * 1024))
        return None

    def run(self, survey_id: str, responses: int, bots: int, memory_value: int, memory_unit: str):
        survey = self.db.get(Pm4d802b91Model, survey_id)
        if not survey:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Encuesta no encontrada.")
        available_slots = Pm4d802b91Service(self.db).available_slots(survey)
        if responses > available_slots:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Solo quedan {available_slots} cupos disponibles para esta encuesta.",
            )

        questions = list(self.db.scalars(
            select(Pm0acc84aeModel).where(Pm0acc84aeModel.pm_4d802b91 == survey_id)
        ))
        if not questions:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La encuesta no tiene preguntas.")
        question_ids = [question.id_universal for question in questions]
        values = list(self.db.scalars(
            select(Pm9a582ff6Model).where(Pm9a582ff6Model.pm_0acc84ae.in_(question_ids))
        ))
        options_by_question = {
            question_id: [value.id_universal for value in values if value.pm_0acc84ae == question_id]
            for question_id in question_ids
        }
        if missing := [question.fd_order for question in questions if not options_by_question[question.id_universal]]:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Las preguntas {', '.join(map(str, missing))} no tienen valores para responder.",
            )

        memory_mb = memory_value * (1024 if memory_unit == "GB" else 1)
        capacity = self.memory_capacity(bots)
        if memory_mb > capacity["max_memory_per_bot_mb"]:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    "La memoria por bot supera el máximo disponible de "
                    f"{capacity['max_memory_per_bot_mb']} MB para {bots} bot(s)."
                ),
            )
        try:
            return asyncio.run(self._run_bots(survey_id, responses, bots, memory_mb))
        except PlaywrightError as error:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Chromium no está disponible en el entorno: {error}",
            ) from error

    async def _run_bots(self, survey_id: str, responses: int, bots: int, memory_mb: int):
        queue: asyncio.Queue[int] = asyncio.Queue()
        for number in range(responses):
            queue.put_nowait(number)
        result: dict[str, int | list[str]] = {
            "requested": responses,
            "completed": 0,
            "failed": 0,
            "bots": min(bots, responses),
            "memory_mb_per_bot": memory_mb,
            "failures": [],
        }
        api_url = settings.bot_api_url.rstrip("/")

        async with async_playwright() as playwright:
            async def worker() -> None:
                browser = await playwright.chromium.launch(
                    headless=True,
                    args=[
                        "--disable-dev-shm-usage",
                        "--renderer-process-limit=1",
                        f"--js-flags=--max-old-space-size={memory_mb}",
                    ],
                )
                try:
                    page = await browser.new_page()
                    await page.goto(f"{api_url}/health", wait_until="domcontentloaded")
                    while True:
                        try:
                            queue.get_nowait()
                        except asyncio.QueueEmpty:
                            break
                        try:
                            await self._complete_one(page, survey_id)
                            result["completed"] = int(result["completed"]) + 1
                        except Exception as error:
                            result["failed"] = int(result["failed"]) + 1
                            failures = result["failures"]
                            if isinstance(failures, list) and len(failures) < 5:
                                failures.append(str(error))
                        finally:
                            queue.task_done()
                finally:
                    await browser.close()

            await asyncio.gather(*(worker() for _ in range(min(bots, responses))))
        return result

    async def _complete_one(self, page: Page, survey_id: str) -> None:
        reservation = await self._request(
            page,
            "/api/public/anonymous",
            "POST",
            {
                "pm_4d802b91": survey_id,
                "fd_reservation_key": f"autofill-{uuid.uuid4()}",
            },
        )
        details = await self._request(page, f"/api/public/surveys/{survey_id}/details", "GET")
        values_by_question: dict[str, list[dict]] = {}
        for value in details["values"]:
            values_by_question.setdefault(value["pm_0acc84ae"], []).append(value)
        for question in details["questions"]:
            values = values_by_question.get(question["id_universal"], [])
            if not values:
                raise RuntimeError(f"La pregunta {question['fd_order']} no tiene valores disponibles.")
            value = values[uuid.uuid4().int % len(values)]
            await self._request(
                page,
                "/api/public/answers",
                "POST",
                {
                    "fd_repply": value["fd_option"],
                    "pm_9a582ff6": value["id_universal"],
                    "pm_1a4a8cd7": reservation["id_universal"],
                },
            )

    async def _request(self, page: Page, path: str, method: str, body: dict | None = None):
        return await page.evaluate(
            """async ({ path, method, body }) => {
                const response = await fetch(path, {
                    method,
                    headers: body ? { 'Content-Type': 'application/json' } : {},
                    body: body ? JSON.stringify(body) : undefined
                });
                const data = await response.json().catch(() => ({}));
                if (!response.ok) throw new Error(data.detail || `HTTP ${response.status}`);
                return data;
            }""",
            {"path": path, "method": method, "body": body},
        )
