from app.controllers.crud_ctrl import create_crud_router
from app.services.pm_3d86d159_srvc import Pm3d86d159Service
from app.schemas.pm_3d86d159_schema import CreateSchema, UpdateSchema, ResponseSchema

router = create_crud_router(
    "/answers", ["Respuestas"], Pm3d86d159Service, CreateSchema, UpdateSchema, ResponseSchema,
    {"list", "page", "create", "update", "delete"},
)
