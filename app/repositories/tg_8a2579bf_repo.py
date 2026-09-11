from app.repositories.base_repo import BaseRepository
from app.models.tg_8a2579bf_model import Tg8a2579bfModel

class Tg8a2579bfRepository(BaseRepository):
    def __init__(self, db): super().__init__(db, Tg8a2579bfModel)
