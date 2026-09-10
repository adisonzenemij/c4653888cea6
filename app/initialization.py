from sqlalchemy import inspect, select, text
from app.config.database import Base, SessionLocal, engine
from app.models.entities_model import *  # Registers all ORM models in Base.metadata.


SEED_DATA = {
    Sd1a9ea48cModel: [
        {"id_universal": "aa72f330-f7b3-4cca-a6ff-a73e7cda780a", "fd_service": "http://localhost:4200"},
        {"id_universal": "0480162b-f665-49a7-9962-551b45e4bb82", "fd_service": "http://127.0.0.1:4200"},
        {"id_universal": "13a40bd4-9a77-459a-b914-3a716f816321", "fd_service": "https://d03f3062e3cf.datacompute.org"},
        {"id_universal": "06456ce1-0fc6-4bce-9fe3-8d649b8e0135", "fd_service": "https://cun-dis38.datacompute.org"},
    ],
    Sd3a731d00Model: [
        {"id_universal": "2ac9e780-9142-475e-9926-72501537ada4", "fd_service": "GET"},
        {"id_universal": "22f2f0d7-3969-4d64-859d-562828752c58", "fd_service": "POST"},
        {"id_universal": "b7c0f396-dfdd-4e7c-bccd-18c865ccf8c5", "fd_service": "PUT"},
        {"id_universal": "e4ce5eb5-7ac2-4db9-831e-7839a991c6d3", "fd_service": "PATCH"},
        {"id_universal": "0e8feba0-bb0d-44c3-93b7-5408fc76dc5e", "fd_service": "DELETE"},
    ],
    Tg5c72c20cModel: [{"id_universal": "001fe2f5-b9aa-4236-bc2e-3f9e1cdbcd72", "fd_login": "root", "fd_passd": "$2y$12$c.RlcM7tlEPEH4DlOgMHYe.GoIWFQH16N199k92zrprLb1OLPnJiy"}],
    Pm8e417bb2Model: [
        {"id_universal": "4c5c8071-5166-4980-a5ad-c72d7a98f17d", "fd_setting": "Publico"},
        {"id_universal": "ca92fde3-6c9e-40fd-b98e-8068cfecb8e1", "fd_setting": "Privado"},
    ],
    Pm0d3dc00eModel: [
        {"id_universal": "ce002c5b-4935-44e0-a7e3-0ba154abc649", "fd_format": "Opciones"},
        {"id_universal": "13a73aaa-733a-43cb-a3bf-33405f5818c0", "fd_format": "Casillas"},
        {"id_universal": "cf6e12ab-2a43-43fb-8251-9a630fa5eba7", "fd_format": "Escala"},
    ],
}


def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        for model, rows in SEED_DATA.items():
            for row in rows:
                if not db.get(model, row["id_universal"]):
                    db.add(model(**row))
        db.commit()


def cors_origins() -> list[str]:
    with SessionLocal() as db:
        return list(db.scalars(select(Sd1a9ea48cModel.fd_service)))
