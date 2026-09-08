from app.repositories.pm_7ea81ec6_repo import Pm7ea81ec6Repository
from app.repositories.pm_0dfa99e2_repo import Pm0dfa99e2Repository
from app.repositories.pm_5d0ddf5b_repo import Pm5d0ddf5bRepository
from app.repositories.sd_3a731d00_repo import Sd3a731d00Repository
from app.services.base_srvc import BaseService
from fastapi import HTTPException, status
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import json


class Pm7ea81ec6Service(BaseService):
    def __init__(self, db):
        super().__init__(Pm7ea81ec6Repository(db), "Sociedad")

    def consult(self, item_id: str) -> dict:
        society = self.get(item_id)
        resources = {
            "vista_360": "Empresas",
            "financieros": "Financieros",
            "situacion_financiera": "Situacion Financiera",
            "resultado_integral": "Resultado Integral",
        }
        result = {
            key: self._query_resource(name, society.fd_document, society.fd_company, key == "vista_360")
            for key, name in resources.items()
        }
        result["vista_360"] = self._limit_vista_360(result["vista_360"], society.fd_document)
        return result

    def _query_resource(self, resource_name: str, document: str, company: str, vista_360: bool) -> dict:
        db = self.repository.db
        resource = Pm5d0ddf5bRepository(db).get_by_name(resource_name)
        if not resource:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"No está configurado el recurso {resource_name}.")
        service = Pm0dfa99e2Repository(db).get(resource.pm_0dfa99e2)
        method = Sd3a731d00Repository(db).get(resource.sd_3a731d00)
        if not service or not method:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"La configuración de {resource_name} está incompleta.")

        if vista_360:
            query = f"*{document} \\- {company}*"
            fields = ["NIT", "nombreEmpresa"]
            source = ["nombreEmpresa", "NIT", "fechaCorte", "puntoEntrada"]
        else:
            query = f"*{document}*"
            fields = ["NIT"]
            source = None
        payload: dict = {
            "size": 15,
            "from": 0,
            "query": {"bool": {"must": [{"query_string": {"fields": fields, "query": query}}]}},
        }
        if source:
            payload["_source"] = source
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

    @staticmethod
    def _limit_vista_360(response: dict, document: str) -> dict:
        hits = response.get("hits", {}).get("hits", [])
        matching = [hit for hit in hits if str(hit.get("_source", {}).get("NIT", "")) == document]
        separated = [hit for hit in matching if "separad" in str(hit.get("_source", {}).get("puntoEntrada", "")).lower()]
        consolidated = [hit for hit in matching if "consolidad" in str(hit.get("_source", {}).get("puntoEntrada", "")).lower()]
        key = lambda hit: str(hit.get("_source", {}).get("fechaCorte", ""))
        selected = sorted(separated, key=key, reverse=True)[:4] + sorted(consolidated, key=key, reverse=True)[:1]
        selected.sort(key=key, reverse=True)
        response["hits"]["hits"] = selected
        response["hits"]["total"] = {"value": len(selected), "relation": "eq"}
        return response
