from app.controllers.crud_ctrl import create_crud_router
from app.services.tg_8a2579bf_srvc import Tg8a2579bfService
from app.schemas.tg_8a2579bf_schema import CreateSchema, UpdateSchema, ResponseSchema
router = create_crud_router("/role-modules", ["Roles Módulos"], Tg8a2579bfService, CreateSchema, UpdateSchema, ResponseSchema)
