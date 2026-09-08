from app.services.base_srvc import BaseService
from app.security.security import pwd_context
from app.repositories.entity_repos import *


class Sd1a9ea48cService(BaseService):
    def __init__(self, db): super().__init__(Sd1a9ea48cRepository(db), "Origen CORS")
class Tg5c72c20cService(BaseService):
    def __init__(self, db): super().__init__(Tg5c72c20cRepository(db), "Usuario")
    def create(self, values):
        values["fd_passd"] = pwd_context.hash(values["fd_passd"])
        return super().create(values)
    def update(self, item_id, values):
        if "fd_passd" in values: values["fd_passd"] = pwd_context.hash(values["fd_passd"])
        return super().update(item_id, values)
class Pm1a4a8cd7Service(BaseService):
    def __init__(self, db): super().__init__(Pm1a4a8cd7Repository(db), "Anónimo")
class Pm8e417bb2Service(BaseService):
    def __init__(self, db): super().__init__(Pm8e417bb2Repository(db), "Alcance")
class Pm0d3dc00eService(BaseService):
    def __init__(self, db): super().__init__(Pm0d3dc00eRepository(db), "Tipo")
class Pm4d802b91Service(BaseService):
    def __init__(self, db): super().__init__(Pm4d802b91Repository(db), "Encuesta")
class Pm0acc84aeService(BaseService):
    def __init__(self, db): super().__init__(Pm0acc84aeRepository(db), "Pregunta")
class Pm9a582ff6Service(BaseService):
    def __init__(self, db): super().__init__(Pm9a582ff6Repository(db), "Valor")
class Pm3d86d159Service(BaseService):
    def __init__(self, db): super().__init__(Pm3d86d159Repository(db), "Respuesta")
