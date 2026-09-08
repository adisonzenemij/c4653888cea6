from app.controllers.crud_ctrl import create_crud_router
from app.services.pm_9a582ff6_srvc import Pm9a582ff6Service
from app.schemas.pm_9a582ff6_schema import CreateSchema, UpdateSchema, ResponseSchema
router = create_crud_router("/values", ["Valores"], Pm9a582ff6Service, CreateSchema, UpdateSchema, ResponseSchema, {"list", "page", "create", "update", "delete"})
