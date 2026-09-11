from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.controllers.crud_ctrl import create_crud_router
from app.repositories.tg_5c72c20c_repo import Tg5c72c20cRepository
from app.schemas.tg_5c72c20c_schema import CreateSchema, UpdateSchema, ResponseSchema, LoginSchema
from app.security.security import create_access_token, verify_password
from app.services.tg_5c72c20c_srvc import Tg5c72c20cService
from app.models.entities_model import Tg2f997592Model, Tg5c72c20cModel, Tg8a26b478Model, Tg8a2579bfModel, Tg9a7bbe6fModel, Ms2e794a8fModel, Ms8b6bd18aModel
from app.dependencies.dependencies import get_current_user

router = APIRouter()


@router.post("/auth/login", tags=["Autenticación"])
def login(payload: LoginSchema, db: Session = Depends(get_db)):
    user = Tg5c72c20cRepository(db).get_by_login(payload.fd_login)
    if not user or not verify_password(payload.fd_passd, user.fd_passd):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    return {"access_token": create_access_token(user.fd_login), "token_type": "bearer"}


@router.get("/auth/permissions", tags=["Autenticación"])
def current_user_permissions(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.scalar(select(Tg5c72c20cModel).where(Tg5c72c20cModel.fd_login == current_user))
    if not user or not user.tg_9a7bbe6f:
        return {"role": None, "permissions": [], "module_permissions": []}
    role = db.get(Tg9a7bbe6fModel, user.tg_9a7bbe6f)
    rows = db.execute(
        select(Ms8b6bd18aModel.fd_product, Ms2e794a8fModel.fd_name, Tg2f997592Model.fd_name, Ms2e794a8fModel.fd_client)
        .join(Tg8a26b478Model, Tg8a26b478Model.ms_2e794a8f == Ms2e794a8fModel.id_universal)
        .join(Tg2f997592Model, Tg2f997592Model.id_universal == Tg8a26b478Model.tg_2f997592)
        .join(Ms8b6bd18aModel, Ms8b6bd18aModel.id_universal == Ms2e794a8fModel.ms_8b6bd18a)
        .where(Tg8a26b478Model.tg_9a7bbe6f == user.tg_9a7bbe6f)
        .order_by(Ms8b6bd18aModel.fd_product, Ms2e794a8fModel.fd_name)
    ).all()
    module_rows = db.execute(
        select(Ms8b6bd18aModel.id_universal, Ms8b6bd18aModel.fd_product, Tg2f997592Model.fd_name)
        .join(Tg8a2579bfModel, Tg8a2579bfModel.ms_8b6bd18a == Ms8b6bd18aModel.id_universal)
        .join(Tg2f997592Model, Tg2f997592Model.id_universal == Tg8a2579bfModel.tg_2f997592)
        .where(Tg8a2579bfModel.tg_9a7bbe6f == user.tg_9a7bbe6f)
        .order_by(Ms8b6bd18aModel.fd_product)
    ).all()
    return {"role": role.fd_name if role else None, "permissions": [
        {"module": module, "resource": resource, "access": access, "client": client}
        for module, resource, access, client in rows
    ], "module_permissions": [
        {"module_id": module_id, "module": module, "access": access}
        for module_id, module, access in module_rows
    ]}

router.include_router(create_crud_router("/users", ["Usuarios"], Tg5c72c20cService, CreateSchema, UpdateSchema, ResponseSchema))
