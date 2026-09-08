from app.controllers.crud_ctrl import create_crud_router
from app.services.pm_0d3dc00e_srvc import Pm0d3dc00eService
from app.schemas.pm_0d3dc00e_schema import CreateSchema, UpdateSchema, ResponseSchema
router = create_crud_router("/types", ["Tipos"], Pm0d3dc00eService, CreateSchema, UpdateSchema, ResponseSchema)
