from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.controllers.crud_ctrl import create_crud_router
from app.models.entities_model import Pm0acc84aeModel, Pm0d3dc00eModel, Pm9a582ff6Model
from app.services.pm_4d802b91_srvc import Pm4d802b91Service
from app.schemas.pm_4d802b91_schema import CreateSchema, UpdateSchema, ResponseSchema
router = create_crud_router("/surveys", ["Encuestas"], Pm4d802b91Service, CreateSchema, UpdateSchema, ResponseSchema, {"list", "page", "create", "update", "delete"})


@router.get("/available", response_model=list[ResponseSchema], summary="Encuestas disponibles")
def list_available_surveys(db: Session = Depends(get_db)):
    return Pm4d802b91Service(db).available()


public_router = APIRouter(prefix="/public/surveys", tags=["Encuestas públicas"])


@public_router.get("/available", response_model=list[ResponseSchema])
def list_public_available_surveys(db: Session = Depends(get_db)):
    return Pm4d802b91Service(db).available()


@public_router.get("/{survey_id}/details")
def public_survey_details(survey_id: str, db: Session = Depends(get_db)):
    questions = list(
        db.scalars(
            select(Pm0acc84aeModel)
            .where(Pm0acc84aeModel.pm_4d802b91 == survey_id)
            .order_by(Pm0acc84aeModel.fd_order)
        )
    )
    question_ids = [question.id_universal for question in questions]
    values = list(
        db.scalars(
            select(Pm9a582ff6Model)
            .where(Pm9a582ff6Model.pm_0acc84ae.in_(question_ids))
            .order_by(Pm9a582ff6Model.fd_order)
        )
    ) if question_ids else []
    type_names = dict(db.execute(select(Pm0d3dc00eModel.id_universal, Pm0d3dc00eModel.fd_format)))
    public_questions = [
        {
            "id_universal": question.id_universal,
            "fd_ask": question.fd_ask,
            "fd_order": question.fd_order,
            "fd_required": question.fd_required,
            "pm_0d3dc00e": question.pm_0d3dc00e,
            "pm_4d802b91": question.pm_4d802b91,
            "fd_format": type_names.get(question.pm_0d3dc00e),
        }
        for question in questions
    ]
    return {"questions": public_questions, "values": values}
