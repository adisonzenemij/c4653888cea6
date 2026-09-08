from app.models.pm_0dfa99e2_model import Pm0dfa99e2Model
from app.repositories.base_repo import BaseRepository


class Pm0dfa99e2Repository(BaseRepository[Pm0dfa99e2Model]):
    def __init__(self, db):
        super().__init__(db, Pm0dfa99e2Model)
