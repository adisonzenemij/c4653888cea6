from app.controllers.crud_ctrl import create_crud_router
from app.services.pm_8e417bb2_srvc import Pm8e417bb2Service
from app.schemas.pm_8e417bb2_schema import CreateSchema, UpdateSchema, ResponseSchema
router = create_crud_router("/scopes", ["Alcances"], Pm8e417bb2Service, CreateSchema, UpdateSchema, ResponseSchema)
