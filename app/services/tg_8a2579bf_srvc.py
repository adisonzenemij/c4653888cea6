from app.services.base_srvc import BaseService
from app.repositories.tg_8a2579bf_repo import Tg8a2579bfRepository

class Tg8a2579bfService(BaseService):
    def __init__(self, db): super().__init__(Tg8a2579bfRepository(db), "Rol módulo")
