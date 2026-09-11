from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.controllers.crud_ctrl import create_crud_router
from app.models.entities_model import Ms2e794a8fModel, Pm0acc84aeModel, Pm0d3dc00eModel, Pm4d802b91Model, Pm9a582ff6Model, Tg2f997592Model, Tg5c72c20cModel, Tg8a26b478Model, Tg9a7bbe6fModel
from app.dependencies.dependencies import get_current_user
from app.services.pm_1a4a8cd7_srvc import Pm1a4a8cd7Service
from app.services.pm_4d802b91_srvc import Pm4d802b91Service
from app.schemas.pm_4d802b91_schema import CreateSchema, UpdateSchema, ResponseSchema
from app.schemas.pm_0acc84ae_schema import CreateSchema as QuestionCreateSchema, UpdateSchema as QuestionUpdateSchema, ResponseSchema as QuestionResponseSchema
from app.schemas.pm_9a582ff6_schema import CreateSchema as ValueCreateSchema, UpdateSchema as ValueUpdateSchema, ResponseSchema as ValueResponseSchema
from app.schemas.survey_autofill_schema import AutoFillSchema
from app.services.pm_0acc84ae_srvc import Pm0acc84aeService
from app.services.pm_9a582ff6_srvc import Pm9a582ff6Service
from app.services.survey_autofill_srvc import SurveyAutoFillService
router = create_crud_router("/surveys", ["Encuestas"], Pm4d802b91Service, CreateSchema, UpdateSchema, ResponseSchema, {"list", "page", "create", "update", "delete"})


def resource_for_table(db: Session, table_name: str) -> Ms2e794a8fModel | None:
    return next((resource for resource in db.scalars(select(Ms2e794a8fModel)) if (
        lambda parts, entity: len(parts) == 5 and f"{entity.split('_', 1)[0]}_{parts[-2]}_{parts[-1]}" == table_name
    )(resource.id_universal.split("-"), resource.fd_entity)), None)


def require_survey_operation(operation: str):
    """Authorize nested survey editors using the survey's CRUD permission."""
    def check(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
        user = db.scalar(select(Tg5c72c20cModel).where(Tg5c72c20cModel.fd_login == current_user))
        survey_resource = resource_for_table(db, Pm4d802b91Model.__tablename__)
        permit = db.scalar(select(Tg8a26b478Model).where(
            Tg8a26b478Model.ms_2e794a8f == (survey_resource.id_universal if survey_resource else None),
            Tg8a26b478Model.tg_9a7bbe6f == (user.tg_9a7bbe6f if user else None),
        ))
        access = db.get(Tg2f997592Model, getattr(permit, f"sd_{operation}", None)) if permit else None
        if not access or access.fd_name != "Permitido":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"No tiene permiso para {operation} en Encuestas.")
    return check


def survey_or_404(survey_id: str, db: Session) -> Pm4d802b91Model:
    survey = db.get(Pm4d802b91Model, survey_id)
    if not survey:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Encuesta no encontrada.")
    return survey


@router.post("/{survey_id}/managed-questions", response_model=QuestionResponseSchema, status_code=status.HTTP_201_CREATED)
def create_managed_question(survey_id: str, payload: QuestionCreateSchema, db: Session = Depends(get_db), _: str = Depends(require_survey_operation("insert"))):
    survey = survey_or_404(survey_id, db)
    question = Pm0acc84aeModel(**payload.model_dump(exclude={"pm_4d802b91"}), pm_4d802b91=survey.id_universal)
    db.add(question)
    survey.fd_query += 1
    db.commit()
    db.refresh(question)
    return question


@router.put("/{survey_id}/managed-questions/{question_id}", response_model=QuestionResponseSchema)
def update_managed_question(survey_id: str, question_id: str, payload: QuestionUpdateSchema, db: Session = Depends(get_db), _: str = Depends(require_survey_operation("update"))):
    survey_or_404(survey_id, db)
    question = db.scalar(select(Pm0acc84aeModel).where(Pm0acc84aeModel.id_universal == question_id, Pm0acc84aeModel.pm_4d802b91 == survey_id))
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pregunta no encontrada en la encuesta.")
    for field, value in payload.model_dump(exclude_unset=True, exclude_none=True, exclude={"pm_4d802b91"}).items():
        setattr(question, field, value)
    db.commit()
    db.refresh(question)
    return question


@router.delete("/{survey_id}/managed-questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_managed_question(survey_id: str, question_id: str, db: Session = Depends(get_db), _: str = Depends(require_survey_operation("delete"))):
    survey = survey_or_404(survey_id, db)
    question = db.scalar(select(Pm0acc84aeModel).where(Pm0acc84aeModel.id_universal == question_id, Pm0acc84aeModel.pm_4d802b91 == survey_id))
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pregunta no encontrada en la encuesta.")
    Pm0acc84aeService(db).delete(question.id_universal)
    survey.fd_query = max(0, survey.fd_query - 1)
    db.commit()


def value_question_or_404(survey_id: str, question_id: str, db: Session) -> Pm0acc84aeModel:
    survey_or_404(survey_id, db)
    question = db.scalar(select(Pm0acc84aeModel).where(Pm0acc84aeModel.id_universal == question_id, Pm0acc84aeModel.pm_4d802b91 == survey_id))
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La pregunta no pertenece a la encuesta.")
    return question


@router.post("/{survey_id}/managed-values", response_model=ValueResponseSchema, status_code=status.HTTP_201_CREATED)
def create_managed_value(survey_id: str, payload: ValueCreateSchema, db: Session = Depends(get_db), _: str = Depends(require_survey_operation("insert"))):
    question = value_question_or_404(survey_id, payload.pm_0acc84ae, db)
    value = Pm9a582ff6Model(fd_option=payload.fd_option, fd_order=payload.fd_order, pm_0acc84ae=question.id_universal)
    db.add(value)
    db.commit()
    db.refresh(value)
    return value


@router.put("/{survey_id}/managed-values/{value_id}", response_model=ValueResponseSchema)
def update_managed_value(survey_id: str, value_id: str, payload: ValueUpdateSchema, db: Session = Depends(get_db), _: str = Depends(require_survey_operation("update"))):
    value = db.scalar(select(Pm9a582ff6Model).join(Pm0acc84aeModel).where(Pm9a582ff6Model.id_universal == value_id, Pm0acc84aeModel.pm_4d802b91 == survey_id))
    if not value:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Valor no encontrado en la encuesta.")
    question_id = payload.pm_0acc84ae if payload.pm_0acc84ae is not None else value.pm_0acc84ae
    value_question_or_404(survey_id, question_id, db)
    for field, field_value in payload.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(value, field, field_value)
    db.commit()
    db.refresh(value)
    return value


@router.delete("/{survey_id}/managed-values/{value_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_managed_value(survey_id: str, value_id: str, db: Session = Depends(get_db), _: str = Depends(require_survey_operation("delete"))):
    value = db.scalar(select(Pm9a582ff6Model).join(Pm0acc84aeModel).where(Pm9a582ff6Model.id_universal == value_id, Pm0acc84aeModel.pm_4d802b91 == survey_id))
    if not value:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Valor no encontrado en la encuesta.")
    Pm9a582ff6Service(db).delete(value.id_universal)


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
