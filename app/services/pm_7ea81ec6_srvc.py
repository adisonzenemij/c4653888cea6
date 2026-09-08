from app.repositories.pm_7ea81ec6_repo import Pm7ea81ec6Repository
from app.services.base_srvc import BaseService


class Pm7ea81ec6Service(BaseService):
    def __init__(self, db):
        super().__init__(Pm7ea81ec6Repository(db), "Sociedad")
