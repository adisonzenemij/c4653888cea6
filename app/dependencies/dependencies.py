from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.security.security import decode_access_token
from app.repositories.tg_5c72c20c_repo import Tg5c72c20cRepository

bearer = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)
):
    subject = decode_access_token(credentials.credentials)
    if not subject or not Tg5c72c20cRepository(db).get_by_login(subject):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o usuario inexistente")
    return subject
