from fastapi import Depends, Response, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.controllers.crud_ctrl import create_crud_router
from app.services.pm_1a4a8cd7_srvc import Pm1a4a8cd7Service
from app.schemas.pm_1a4a8cd7_schema import (
    CreateSchema,
    ReleaseReservationSchema,
    ResponseSchema,
    UpdateSchema,
)
router = create_crud_router("/anonymous", ["Anónimos"], Pm1a4a8cd7Service, CreateSchema, UpdateSchema, ResponseSchema, {"list", "page", "create", "update", "delete"})


@router.post("/{item_id}/release", status_code=status.HTTP_204_NO_CONTENT)
def release_reservation(
    item_id: str,
    payload: ReleaseReservationSchema,
    db: Session = Depends(get_db),
):
    Pm1a4a8cd7Service(db).release(item_id, payload.fd_reservation_key)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{item_id}/renew", response_model=ResponseSchema)
def renew_reservation(
    item_id: str,
    payload: ReleaseReservationSchema,
    db: Session = Depends(get_db),
):
    return Pm1a4a8cd7Service(db).renew(item_id, payload.fd_reservation_key)
