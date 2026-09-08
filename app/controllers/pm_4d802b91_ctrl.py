from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.controllers.crud_ctrl import create_crud_router
from app.services.pm_4d802b91_srvc import Pm4d802b91Service
from app.schemas.pm_4d802b91_schema import CreateSchema, UpdateSchema, ResponseSchema
router = create_crud_router("/surveys", ["Encuestas"], Pm4d802b91Service, CreateSchema, UpdateSchema, ResponseSchema, {"list", "page", "create", "update", "delete"})


@router.get("/available", response_model=list[ResponseSchema], summary="Encuestas disponibles")
def list_available_surveys(db: Session = Depends(get_db)):
    return Pm4d802b91Service(db).available()
