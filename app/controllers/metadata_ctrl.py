from pydantic import BaseModel, Field

from app.controllers.crud_ctrl import create_crud_router
from app.repositories.base_repo import BaseRepository
from app.services.base_srvc import BaseService
from app.models.entities_model import Sd6bb63bb4Model, Ms8b6bd18aModel, Ms2e794a8fModel, Tg9a7bbe6fModel, Tg2f997592Model, Tg8a26b478Model
from app.schemas.base_schema import OutputSchema


def service_for(model, label):
    return lambda db: BaseService(BaseRepository(db, model), label)

class NameCreate(BaseModel): fd_name: str = Field(max_length=50)
class NameUpdate(BaseModel): fd_name: str | None = Field(default=None, max_length=50)
class NameResponse(NameCreate, OutputSchema): pass
class ModuleCreate(BaseModel): fd_client: str = Field(max_length=8); fd_prefix: str = Field(max_length=250); fd_product: str = Field(max_length=250)
class ModuleUpdate(BaseModel): fd_client: str | None = None; fd_prefix: str | None = None; fd_product: str | None = None
class ModuleResponse(ModuleCreate, OutputSchema): pass
class ResourceCreate(BaseModel):
    fd_client: str = Field(max_length=8); fd_entity: str = Field(max_length=250); fd_name: str = Field(max_length=250); sd_select: str; sd_insert: str; sd_update: str; sd_delete: str; ms_8b6bd18a: str
class ResourceUpdate(BaseModel):
    fd_client: str | None = None; fd_entity: str | None = None; fd_name: str | None = None; sd_select: str | None = None; sd_insert: str | None = None; sd_update: str | None = None; sd_delete: str | None = None; ms_8b6bd18a: str | None = None
class ResourceResponse(ResourceCreate, OutputSchema): pass
class PermitCreate(BaseModel): ms_2e794a8f: str; tg_2f997592: str; tg_9a7bbe6f: str
class PermitUpdate(BaseModel): ms_2e794a8f: str | None = None; tg_2f997592: str | None = None; tg_9a7bbe6f: str | None = None
class PermitResponse(PermitCreate, OutputSchema): pass

jwt_router = create_crud_router('/jwt-permits', ['JWT Permisos'], service_for(Sd6bb63bb4Model, 'Permiso JWT'), NameCreate, NameUpdate, NameResponse)
module_router = create_crud_router('/table-modules', ['Entidades Módulos'], service_for(Ms8b6bd18aModel, 'Módulo'), ModuleCreate, ModuleUpdate, ModuleResponse)
resource_router = create_crud_router('/table-resources', ['Entidades Recursos'], service_for(Ms2e794a8fModel, 'Recurso de tabla'), ResourceCreate, ResourceUpdate, ResourceResponse)
role_data_router = create_crud_router('/role-data', ['Roles Datos'], service_for(Tg9a7bbe6fModel, 'Rol de datos'), NameCreate, NameUpdate, NameResponse)
role_access_router = create_crud_router('/role-access', ['Roles Accesos'], service_for(Tg2f997592Model, 'Rol de acceso'), NameCreate, NameUpdate, NameResponse)
role_permit_router = create_crud_router('/role-permits', ['Roles Permisos'], service_for(Tg8a26b478Model, 'Permiso por rol'), PermitCreate, PermitUpdate, PermitResponse)
