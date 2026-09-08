from sqlalchemy import select
from app.repositories.base_repo import BaseRepository
from app.models.entities_model import (
    Sd1a9ea48cModel, Tg5c72c20cModel, Pm1a4a8cd7Model, Pm8e417bb2Model,
    Pm0d3dc00eModel, Pm4d802b91Model, Pm0acc84aeModel, Pm9a582ff6Model, Pm3d86d159Model,
)


class Sd1a9ea48cRepository(BaseRepository):
    def __init__(self, db): super().__init__(db, Sd1a9ea48cModel)


class Tg5c72c20cRepository(BaseRepository):
    def __init__(self, db): super().__init__(db, Tg5c72c20cModel)
    def get_by_login(self, login: str): return self.db.scalar(select(self.model).where(self.model.fd_login == login))


class Pm1a4a8cd7Repository(BaseRepository):
    def __init__(self, db): super().__init__(db, Pm1a4a8cd7Model)


class Pm8e417bb2Repository(BaseRepository):
    def __init__(self, db): super().__init__(db, Pm8e417bb2Model)


class Pm0d3dc00eRepository(BaseRepository):
    def __init__(self, db): super().__init__(db, Pm0d3dc00eModel)


class Pm4d802b91Repository(BaseRepository):
    def __init__(self, db): super().__init__(db, Pm4d802b91Model)


class Pm0acc84aeRepository(BaseRepository):
    def __init__(self, db): super().__init__(db, Pm0acc84aeModel)


class Pm9a582ff6Repository(BaseRepository):
    def __init__(self, db): super().__init__(db, Pm9a582ff6Model)


class Pm3d86d159Repository(BaseRepository):
    def __init__(self, db): super().__init__(db, Pm3d86d159Model)
