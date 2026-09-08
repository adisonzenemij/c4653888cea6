from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.controllers.crud_ctrl import create_crud_router
from app.repositories.tg_5c72c20c_repo import Tg5c72c20cRepository
from app.schemas.tg_5c72c20c_schema import CreateSchema, UpdateSchema, ResponseSchema, LoginSchema
from app.security.security import create_access_token, verify_password
from app.services.tg_5c72c20c_srvc import Tg5c72c20cService

router = APIRouter()


@router.post("/auth/login", tags=["Autenticación"])
def login(payload: LoginSchema, db: Session = Depends(get_db)):
    user = Tg5c72c20cRepository(db).get_by_login(payload.fd_login)
    if not user or not verify_password(payload.fd_passd, user.fd_passd):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    return {"access_token": create_access_token(user.fd_login), "token_type": "bearer"}

router.include_router(create_crud_router("/users", ["Usuarios"], Tg5c72c20cService, CreateSchema, UpdateSchema, ResponseSchema))
