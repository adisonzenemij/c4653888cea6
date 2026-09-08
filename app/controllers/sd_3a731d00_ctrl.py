from app.controllers.crud_ctrl import create_crud_router
from app.schemas.sd_3a731d00_schema import CreateSchema, ResponseSchema, UpdateSchema
from app.services.sd_3a731d00_srvc import Sd3a731d00Service


router = create_crud_router(
    "/methods", ["Métodos"], Sd3a731d00Service, CreateSchema, UpdateSchema, ResponseSchema
)
