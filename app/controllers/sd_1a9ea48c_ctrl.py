from app.controllers.crud_ctrl import create_crud_router
from app.services.sd_1a9ea48c_srvc import Sd1a9ea48cService
from app.schemas.sd_1a9ea48c_schema import CreateSchema, UpdateSchema, ResponseSchema
router = create_crud_router("/cors-origins", ["Orígenes CORS"], Sd1a9ea48cService, CreateSchema, UpdateSchema, ResponseSchema)
