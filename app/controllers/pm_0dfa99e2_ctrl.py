from app.controllers.crud_ctrl import create_crud_router
from app.schemas.pm_0dfa99e2_schema import CreateSchema, ResponseSchema, UpdateSchema
from app.services.pm_0dfa99e2_srvc import Pm0dfa99e2Service


router = create_crud_router(
    "/services", ["Servicios"], Pm0dfa99e2Service, CreateSchema, UpdateSchema, ResponseSchema
)
