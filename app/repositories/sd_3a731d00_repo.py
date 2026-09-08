from app.models.sd_3a731d00_model import Sd3a731d00Model
from app.repositories.base_repo import BaseRepository


class Sd3a731d00Repository(BaseRepository[Sd3a731d00Model]):
    def __init__(self, db):
        super().__init__(db, Sd3a731d00Model)
