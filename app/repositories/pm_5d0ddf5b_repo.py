from app.models.pm_5d0ddf5b_model import Pm5d0ddf5bModel
from app.repositories.base_repo import BaseRepository
from sqlalchemy import select


class Pm5d0ddf5bRepository(BaseRepository[Pm5d0ddf5bModel]):
    def __init__(self, db):
        super().__init__(db, Pm5d0ddf5bModel)

    def get_by_name(self, name: str):
        return self.db.scalar(select(self.model).where(self.model.fd_name == name))
