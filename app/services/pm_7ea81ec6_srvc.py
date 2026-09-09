import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

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
