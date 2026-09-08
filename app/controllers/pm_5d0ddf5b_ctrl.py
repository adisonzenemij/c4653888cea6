from app.controllers.crud_ctrl import create_crud_router
from app.schemas.pm_5d0ddf5b_schema import CreateSchema, ResponseSchema, UpdateSchema
from app.services.pm_5d0ddf5b_srvc import Pm5d0ddf5bService


router = create_crud_router(
    "/resources", ["Recursos"], Pm5d0ddf5bService, CreateSchema, UpdateSchema, ResponseSchema
)
