from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.pm_1a4a8cd7_schema import CreateSchema as AnonymousCreateSchema, ResponseSchema as AnonymousResponseSchema
from app.schemas.pm_3d86d159_schema import CreateSchema as AnswerCreateSchema, ResponseSchema as AnswerResponseSchema
from app.services.pm_1a4a8cd7_srvc import Pm1a4a8cd7Service
from app.services.pm_3d86d159_srvc import Pm3d86d159Service


router = APIRouter(prefix="/public", tags=["Participación Pública"])


@router.post("/anonymous", response_model=AnonymousResponseSchema, status_code=status.HTTP_201_CREATED)
def reserve_anonymous_participation(payload: AnonymousCreateSchema, db: Session = Depends(get_db)):
    return Pm1a4a8cd7Service(db).create(payload.model_dump())


@router.post("/answers", response_model=AnswerResponseSchema, status_code=status.HTTP_201_CREATED)
def create_public_answer(payload: AnswerCreateSchema, db: Session = Depends(get_db)):
    return Pm3d86d159Service(db).create(payload.model_dump())
