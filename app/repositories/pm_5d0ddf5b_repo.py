from app.models.pm_5d0ddf5b_model import Pm5d0ddf5bModel
from app.repositories.base_repo import BaseRepository


class Pm5d0ddf5bRepository(BaseRepository[Pm5d0ddf5bModel]):
    def __init__(self, db):
        super().__init__(db, Pm5d0ddf5bModel)
