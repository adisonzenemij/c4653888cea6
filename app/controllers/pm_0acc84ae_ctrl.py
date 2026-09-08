from app.controllers.crud_ctrl import create_crud_router
from app.services.pm_0acc84ae_srvc import Pm0acc84aeService
from app.schemas.pm_0acc84ae_schema import CreateSchema, UpdateSchema, ResponseSchema
router = create_crud_router("/questions", ["Preguntas"], Pm0acc84aeService, CreateSchema, UpdateSchema, ResponseSchema, {"list", "page", "create", "update", "delete"})
