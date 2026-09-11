from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.controllers.crud_ctrl import create_crud_router
from app.models.entities_model import Pm0acc84aeModel, Pm0d3dc00eModel, Pm9a582ff6Model, Tg5c72c20cModel, Tg9a7bbe6fModel
from app.dependencies.dependencies import get_current_user
from app.services.pm_1a4a8cd7_srvc import Pm1a4a8cd7Service
from app.services.pm_4d802b91_srvc import Pm4d802b91Service
from app.schemas.pm_4d802b91_schema import CreateSchema, UpdateSchema, ResponseSchema
from app.schemas.survey_autofill_schema import AutoFillSchema
from app.services.survey_autofill_srvc import SurveyAutoFillService
router = create_crud_router("/surveys", ["Encuestas"], Pm4d802b91Service, CreateSchema, UpdateSchema, ResponseSchema, {"list", "page", "create", "update", "delete"})


def require_master(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> str:
    role_name = db.scalar(
        select(Tg9a7bbe6fModel.fd_name)
        .join(Tg5c72c20cModel, Tg5c72c20cModel.tg_9a7bbe6f == Tg9a7bbe6fModel.id_universal)
        .where(Tg5c72c20cModel.fd_login == current_user)
    )
    if role_name != "Master":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Autocompletar solo está disponible para el rol Master.")
    return current_user


@router.get("/autofill-capacity", summary="Capacidad de memoria para bots")
def autofill_capacity(bots: int = Query(1, ge=1, le=10), _: str = Depends(require_master)):
    return SurveyAutoFillService.memory_capacity(bots)


@router.post("/{survey_id}/autofill", summary="Autocompletar encuesta con Chromium")
def autofill_survey(survey_id: str, payload: AutoFillSchema, db: Session = Depends(get_db), _: str = Depends(require_master)):
    return SurveyAutoFillService(db).run(survey_id, **payload.model_dump())


@router.get("/available", response_model=list[ResponseSchema], summary="Encuestas disponibles")
def list_available_surveys(db: Session = Depends(get_db)):
    return Pm4d802b91Service(db).available()


public_router = APIRouter(prefix="/public/surveys", tags=["Encuestas públicas"])


@public_router.get("/available", response_model=list[ResponseSchema])
def list_public_available_surveys(db: Session = Depends(get_db)):
    return Pm4d802b91Service(db).available()


@public_router.get("/resume/{survey_id}")
def resume_public_survey(survey_id: str, reservation_key: str, db: Session = Depends(get_db)):
    reservation = Pm1a4a8cd7Service(db).resume(survey_id, reservation_key)
    survey = Pm4d802b91Service(db).get(survey_id)
    return {
        "survey": {
            "id_universal": survey.id_universal,
            "fd_count": survey.fd_count,
            "fd_name": survey.fd_name,
            "fd_query": survey.fd_query,
            "fd_since": survey.fd_since,
            "fd_until": survey.fd_until,
            "pm_8e417bb2": survey.pm_8e417bb2,
            "fd_available_slots": Pm4d802b91Service(db).available_slots(survey),
        },
        "reservation": {
            "id_universal": reservation.id_universal,
            "fd_random": reservation.fd_random,
            "pm_4d802b91": reservation.pm_4d802b91,
            "fd_reservation_key": reservation.fd_reservation_key,
        },
    }


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
    type_names = dict(
        db.execute(select(Pm0d3dc00eModel.id_universal, Pm0d3dc00eModel.fd_format)).all()
    )
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
