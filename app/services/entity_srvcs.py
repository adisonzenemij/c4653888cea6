import secrets
import string
from datetime import date, datetime, time, timedelta

from fastapi import HTTPException, status
from sqlalchemy import func, select

from app.models.entities_model import Pm1a4a8cd7Model, Pm3d86d159Model, Pm4d802b91Model
from app.services.base_srvc import BaseService
from app.security.security import pwd_context
from app.repositories.entity_repos import *


class Sd1a9ea48cService(BaseService):
    def __init__(self, db): super().__init__(Sd1a9ea48cRepository(db), "Origen CORS")
class Tg5c72c20cService(BaseService):
    def __init__(self, db): super().__init__(Tg5c72c20cRepository(db), "Usuario")
    def create(self, values):
        values["fd_passd"] = pwd_context.hash(values["fd_passd"])
        return super().create(values)
    def update(self, item_id, values):
        if "fd_passd" in values: values["fd_passd"] = pwd_context.hash(values["fd_passd"])
        return super().update(item_id, values)
class Pm1a4a8cd7Service(BaseService):
    def __init__(self, db): super().__init__(Pm1a4a8cd7Repository(db), "Anónimo")

    @staticmethod
    def _has_answers(db, anonymous_id: str) -> bool:
        return bool(
            db.scalar(
                select(func.count())
                .select_from(Pm3d86d159Model)
                .where(Pm3d86d159Model.pm_1a4a8cd7 == anonymous_id)
            )
        )

    def _release_expired_reservations(self, survey_id: str, now: datetime) -> None:
        db = self.repository.db
        expired = list(
            db.scalars(
                select(Pm1a4a8cd7Model).where(
                    Pm1a4a8cd7Model.pm_4d802b91 == survey_id,
                    Pm1a4a8cd7Model.fd_reserved_until.is_not(None),
                    Pm1a4a8cd7Model.fd_reserved_until < now,
                )
            )
        )
        for reservation in expired:
            if not self._has_answers(db, reservation.id_universal):
                db.delete(reservation)
        db.flush()

    def create(self, values):
        survey_id = values.get("pm_4d802b91")
        reservation_key = values.get("fd_reservation_key")
        if not survey_id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Debe indicar la encuesta que se va a responder.",
            )
        if not reservation_key:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Debe indicar la clave de reserva de la encuesta.",
            )

        db = self.repository.db
        # Serializes concurrent attempts against one survey until the anonymous
        # participation has been committed, so fd_count cannot be exceeded.
        survey = db.scalar(
            select(Pm4d802b91Model)
            .where(Pm4d802b91Model.id_universal == survey_id)
            .with_for_update()
        )
        if not survey:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Encuesta no encontrada.",
            )

        try:
            opening = datetime.combine(
                date.fromisoformat(survey.fd_since[:10]), time.min
            )
            closing = datetime.combine(
                # Include the entire closing day, through 23:59:59.
                date.fromisoformat(survey.fd_until[:10]), time.max
            )
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="La encuesta tiene fechas de disponibilidad inválidas.",
            )

        now = datetime.now()
        if now < opening:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="La encuesta aún no está disponible.",
            )
        if now > closing:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="La encuesta ya no está disponible.",
            )

        self._release_expired_reservations(survey.id_universal, now)

        # Retrying an open action with the same browser key returns the same
        # reservation instead of consuming another slot.
        reservation = db.scalar(
            select(Pm1a4a8cd7Model).where(
                Pm1a4a8cd7Model.pm_4d802b91 == survey.id_universal,
                Pm1a4a8cd7Model.fd_reservation_key == reservation_key,
            )
        )
        if reservation:
            if self._has_answers(db, reservation.id_universal):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Esta encuesta ya fue enviada desde esta sesión.",
                )
            reservation.fd_reserved_until = now + timedelta(minutes=30)
            db.commit()
            db.refresh(reservation)
            return reservation

        used_slots = db.scalar(
            select(func.count())
            .select_from(Pm1a4a8cd7Model)
            .where(Pm1a4a8cd7Model.pm_4d802b91 == survey.id_universal)
        ) or 0
        if used_slots >= survey.fd_count:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="La encuesta alcanzó el número máximo de participaciones.",
            )

        # The server creates the anonymous identity; a client cannot choose it.
        values["fd_random"] = "".join(
            secrets.choice(string.ascii_letters + string.digits) for _ in range(50)
        )
        values["fd_reserved_until"] = now + timedelta(minutes=30)
        return super().create(values)

    def release(self, item_id: str, reservation_key: str) -> None:
        reservation = self.get(item_id)
        if reservation.fd_reservation_key != reservation_key:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="La reserva no pertenece a esta sesión.",
            )
        if self._has_answers(self.repository.db, reservation.id_universal):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede liberar una encuesta que ya tiene respuestas.",
            )
        self.repository.delete(reservation)

    def renew(self, item_id: str, reservation_key: str):
        reservation = self.get(item_id)
        if reservation.fd_reservation_key != reservation_key:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="La reserva no pertenece a esta sesión.",
            )
        if self._has_answers(self.repository.db, reservation.id_universal):
            return reservation
        reservation.fd_reserved_until = datetime.now() + timedelta(minutes=30)
        self.repository.db.commit()
        self.repository.db.refresh(reservation)
        return reservation
class Pm8e417bb2Service(BaseService):
    def __init__(self, db): super().__init__(Pm8e417bb2Repository(db), "Alcance")
class Pm0d3dc00eService(BaseService):
    def __init__(self, db): super().__init__(Pm0d3dc00eRepository(db), "Tipo")
class Pm4d802b91Service(BaseService):
    def __init__(self, db): super().__init__(Pm4d802b91Repository(db), "Encuesta")

    def available(self):
        """Returns surveys that can still receive a new anonymous response."""
        today = date.today()
        now = datetime.now()
        available_surveys = []
        for survey in super().list():
            try:
                opening = date.fromisoformat(survey.fd_since[:10])
                closing = date.fromisoformat(survey.fd_until[:10])
            except (TypeError, ValueError):
                continue
            if not opening <= today <= closing:
                continue

            participations = list(
                self.repository.db.scalars(
                    select(Pm1a4a8cd7Model).where(
                        Pm1a4a8cd7Model.pm_4d802b91 == survey.id_universal
                    )
                )
            )
            used_slots = sum(
                participation.fd_reserved_until is None
                or participation.fd_reserved_until >= now
                or Pm1a4a8cd7Service._has_answers(
                    self.repository.db, participation.id_universal
                )
                for participation in participations
            )
            if used_slots < survey.fd_count:
                available_surveys.append(survey)
        return available_surveys
class Pm0acc84aeService(BaseService):
    def __init__(self, db): super().__init__(Pm0acc84aeRepository(db), "Pregunta")
class Pm9a582ff6Service(BaseService):
    def __init__(self, db): super().__init__(Pm9a582ff6Repository(db), "Valor")
class Pm3d86d159Service(BaseService):
    def __init__(self, db): super().__init__(Pm3d86d159Repository(db), "Respuesta")
