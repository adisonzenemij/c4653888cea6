from app.controllers.crud_ctrl import create_crud_router
from fastapi import Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.pm_7ea81ec6_schema import CreateSchema, ResponseSchema, UpdateSchema
from app.services.pm_7ea81ec6_srvc import Pm7ea81ec6Service


router = create_crud_router(
    "/societies", ["Sociedades"], Pm7ea81ec6Service, CreateSchema, UpdateSchema, ResponseSchema
)


@router.post("/{item_id}/consult")
def consult_society(item_id: str, db: Session = Depends(get_db)):
    return Pm7ea81ec6Service(db).consult(item_id)
