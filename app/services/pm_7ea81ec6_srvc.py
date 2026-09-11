import json
import re
from http.cookiejar import CookieJar
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, Request, build_opener, urlopen

from fastapi import HTTPException, status

from app.repositories.pm_0dfa99e2_repo import Pm0dfa99e2Repository
from app.repositories.pm_5d0ddf5b_repo import Pm5d0ddf5bRepository
from app.repositories.pm_7ea81ec6_repo import Pm7ea81ec6Repository
from app.repositories.sd_3a731d00_repo import Sd3a731d00Repository
from app.services.base_srvc import BaseService


class Pm7ea81ec6Service(BaseService):
    def __init__(self, db):
        super().__init__(Pm7ea81ec6Repository(db), "Sociedad")

    def consult(self, item_id: str) -> dict:
        society = self.get(item_id)
        vista_360 = self._limit_vista_360(
            self._query_vista_360(society.fd_document, society.fd_company), society.fd_document
        )
        cutoffs = [
            hit.get("_source", {}).get("fechaCorte")
            for hit in vista_360.get("hits", {}).get("hits", [])
            if hit.get("_source", {}).get("fechaCorte")
        ]
        return {
            "vista_360": vista_360,
            "financieros": self._query_by_cutoff("Financieros", society.fd_document, cutoffs),
            "situacion_financiera": self._query_by_cutoff("Situacion Financiera", society.fd_document, cutoffs),
            "resultado_integral": self._query_by_cutoff("Resultado Integral", society.fd_document, cutoffs),
        }

    def consult_rues(self, item_id: str) -> dict:
        """Consulta la información mercantil RUES de la empresa seleccionada."""
        society = self.get(item_id)
        return self._rues_post("Consulta NIT", {
            "txtNIT": society.fd_document,
            "txtCI": "",
            "txtDV": "",
        })

    def consult_rues_owners(self, item_id: str, codigo_camara: str, matricula: str) -> dict:
        """Consulta propietarios y establecimientos de una matrícula RUES."""
        self.get(item_id)  # Verifica que la empresa exista antes de consultar el servicio externo.
        if not codigo_camara.isdigit() or not matricula.isdigit():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="La cámara y matrícula RUES deben ser numéricas.")
        return self._rues_post("Propietario | Establecimientos", {
            "codigo_camara": codigo_camara,
            "matricula": matricula,
        })

    def _query_vista_360(self, document: str, company: str) -> dict:
        payload = {
            "size": 15,
            "from": 0,
            "query": {
                "bool": {
                    "must": [{"query_string": {
                        "fields": ["NIT", "nombreEmpresa"],
                        "query": f"*{document} \\- {company}*",
                    }}]
                }
            },
            "_source": ["nombreEmpresa", "NIT", "fechaCorte", "puntoEntrada"],
        }
        return self._request("Empresas", payload)

    def _query_by_cutoff(self, resource_name: str, document: str, cutoffs: list[str]) -> dict:
        return {
            cutoff: self._query_resource_by_cutoff(resource_name, document, cutoff)
            for cutoff in cutoffs
        }

    def _query_resource_by_cutoff(self, resource_name: str, document: str, cutoff: str) -> dict:
        if resource_name == "Financieros":
            terms = [
                {"term": {"NIT.keyword": document}},
                {"term": {"fechaCorte": cutoff}},
                {"term": {"infoEmpresa.puntoEntrada.keyword": "Plenas-Separados"}},
            ]
        else:
            terms = [
                {"term": {"infoEmpresa.NIT.keyword": document}},
                {"term": {"infoEmpresa.corte": cutoff}},
                {"term": {"infoEmpresa.puntoEntrada.keyword": "Plenas-Separados"}},
            ]
        return self._request(resource_name, {"size": 1, "query": {"bool": {"must": terms}}})

    def _request(self, resource_name: str, payload: dict) -> dict:
        db = self.repository.db
        resource = Pm5d0ddf5bRepository(db).get_by_name(resource_name)
        if not resource:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"No está configurado el recurso {resource_name}.")
        service = Pm0dfa99e2Repository(db).get(resource.pm_0dfa99e2)
        method = Sd3a731d00Repository(db).get(resource.sd_3a731d00)
        if not service or not method:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"La configuración de {resource_name} está incompleta.")

        url = f"{service.fd_service.rstrip('/')}/{resource.fd_path.lstrip('/')}"
        request = Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            method=method.fd_service.upper(),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
        try:
            with urlopen(request, timeout=20) as response:
                return json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"No fue posible consultar {resource_name}: {error}",
            ) from error

    def _rues_post(self, resource_name: str, fields: dict[str, str]) -> dict:
        """Abre la sesión RUES, obtiene el antiforgery token y ejecuta un POST form-url-encoded."""
        db = self.repository.db
        resource = Pm5d0ddf5bRepository(db).get_by_name(resource_name)
        if not resource:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"No está configurado el recurso RUES {resource_name}.")
        service = Pm0dfa99e2Repository(db).get(resource.pm_0dfa99e2)
        method = Sd3a731d00Repository(db).get(resource.sd_3a731d00)
        if not service or not method or method.fd_service.upper() != "POST":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"La configuración del recurso RUES {resource_name} es inválida.")

        base_url = service.fd_service.rstrip("/")
        home_url = f"{base_url}/"
        endpoint = f"{base_url}/{resource.fd_path.lstrip('/')}"
        cookie_jar = CookieJar()
        opener = build_opener(HTTPCookieProcessor(cookie_jar))
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (compatible; CUN-Intelligence-Business/1.0)",
        }
        try:
            with opener.open(Request(home_url, headers=headers), timeout=20) as response:
                html = response.read().decode("utf-8", errors="replace")
            token = self._rues_token(html)
            if not token:
                raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="RUES no entregó el token de verificación requerido.")
            body = urlencode({"__RequestVerificationToken": token, **fields}).encode("utf-8")
            request = Request(endpoint, data=body, method="POST", headers={
                **headers,
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Referer": home_url,
                "X-Requested-With": "XMLHttpRequest",
            })
            with opener.open(request, timeout=25) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPException:
            raise
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"No fue posible consultar RUES: {error}",
            ) from error

    @staticmethod
    def _rues_token(html: str) -> str | None:
        patterns = (
            r'<input[^>]*name=["\']__RequestVerificationToken["\'][^>]*value=["\']([^"\']+)',
            r'<input[^>]*value=["\']([^"\']+)["\'][^>]*name=["\']__RequestVerificationToken["\']',
        )
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                return match.group(1)
        return None

    @staticmethod
    def _limit_vista_360(response: dict, document: str) -> dict:
        hits = response.get("hits", {}).get("hits", [])
        matching = [hit for hit in hits if str(hit.get("_source", {}).get("NIT", "")) == document]
        separated = [
            hit for hit in matching
            if "separad" in str(hit.get("_source", {}).get("puntoEntrada", "")).lower()
        ]
        key = lambda hit: str(hit.get("_source", {}).get("fechaCorte", ""))
        selected = sorted(separated, key=key, reverse=True)[:5]
        response["hits"]["hits"] = selected
        response["hits"]["total"] = {"value": len(selected), "relation": "eq"}
        return response
