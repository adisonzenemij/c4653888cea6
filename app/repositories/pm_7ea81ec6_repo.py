from app.models.pm_7ea81ec6_model import Pm7ea81ec6Model
from app.repositories.base_repo import BaseRepository


class Pm7ea81ec6Repository(BaseRepository[Pm7ea81ec6Model]):
    def __init__(self, db):
        super().__init__(db, Pm7ea81ec6Model)
