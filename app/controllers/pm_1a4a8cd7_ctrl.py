from app.controllers.crud_ctrl import create_crud_router
from app.services.pm_1a4a8cd7_srvc import Pm1a4a8cd7Service
from app.schemas.pm_1a4a8cd7_schema import CreateSchema, UpdateSchema, ResponseSchema
router = create_crud_router("/anonymous", ["Anónimos"], Pm1a4a8cd7Service, CreateSchema, UpdateSchema, ResponseSchema, {"list", "page", "create", "update", "delete"})
