from app.controllers.crud_ctrl import create_crud_router
from app.schemas.pm_7ea81ec6_schema import CreateSchema, ResponseSchema, UpdateSchema
from app.services.pm_7ea81ec6_srvc import Pm7ea81ec6Service


router = create_crud_router(
    "/societies", ["Sociedades"], Pm7ea81ec6Service, CreateSchema, UpdateSchema, ResponseSchema
)
