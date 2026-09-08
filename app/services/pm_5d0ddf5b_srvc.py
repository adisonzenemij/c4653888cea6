from app.repositories.pm_5d0ddf5b_repo import Pm5d0ddf5bRepository
from app.services.base_srvc import BaseService


class Pm5d0ddf5bService(BaseService):
    def __init__(self, db):
        super().__init__(Pm5d0ddf5bRepository(db), "Recurso")
