from app.repositories.sd_3a731d00_repo import Sd3a731d00Repository
from app.services.base_srvc import BaseService


class Sd3a731d00Service(BaseService):
    def __init__(self, db):
        super().__init__(Sd3a731d00Repository(db), "Método")
