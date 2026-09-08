from app.repositories.pm_0dfa99e2_repo import Pm0dfa99e2Repository
from app.services.base_srvc import BaseService


class Pm0dfa99e2Service(BaseService):
    def __init__(self, db):
        super().__init__(Pm0dfa99e2Repository(db), "Servicio")
