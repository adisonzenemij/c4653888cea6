from typing import Callable
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.dependencies.dependencies import get_current_user
from app.models.entities_model import Ms2e794a8fModel, Tg2f997592Model, Tg5c72c20cModel, Tg8a26b478Model


def create_crud_router(
    prefix: str, tags: list[str], service_factory: Callable, create_schema: type[BaseModel],
    update_schema: type[BaseModel], response_schema: type[BaseModel], operations: set[str] | None = None,
) -> APIRouter:
    """Creates the HTTP controller; business logic remains in its service."""
    operations = operations or {"list", "page", "create", "update", "delete"}
    router = APIRouter(prefix=prefix, tags=tags, dependencies=[Depends(get_current_user)])

    def require_operation(operation: str):
        def check(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
            model = service_factory(db).repository.model
            table_name = model.__tablename__
            resource = next((item for item in db.scalars(select(Ms2e794a8fModel)) if (
                lambda parts, entity: len(parts) == 5 and f"{entity.split('_', 1)[0]}_{parts[-2]}_{parts[-1]}" == table_name
            )(item.id_universal.split("-"), item.fd_entity)), None)
            user = db.scalar(select(Tg5c72c20cModel).where(Tg5c72c20cModel.fd_login == current_user))
            permit = db.scalar(select(Tg8a26b478Model).where(
                Tg8a26b478Model.ms_2e794a8f == resource.id_universal if resource else False,
                Tg8a26b478Model.tg_9a7bbe6f == (user.tg_9a7bbe6f if user else None),
            ))
            access = db.get(Tg2f997592Model, getattr(permit, f"sd_{operation}", None)) if permit else None
            if not access or access.fd_name != "Permitido":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"No tiene permiso para {operation} en este recurso.")
        return check

    if "list" in operations:
        def list_items(db: Session = Depends(get_db)):
            return service_factory(db).list()
        router.add_api_route("/", list_items, methods=["GET"], response_model=list[response_schema], summary="Select normal")

    if "page" in operations:
        def page_items(offset: int = Query(0, ge=0), limit: int = Query(25, ge=1, le=100), db: Session = Depends(get_db)):
            items, total = service_factory(db).page(offset, limit)
            return jsonable_encoder(
                {"offset": offset, "limit": limit, "total": total, "items": items}
            )
        router.add_api_route("/page", page_items, methods=["GET"], response_model=dict, summary="Select paginado")

    if "create" in operations:
        def create_item(payload: create_schema, db: Session = Depends(get_db)):
            return service_factory(db).create(payload.model_dump())
        router.add_api_route("/", create_item, methods=["POST"], response_model=response_schema, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_operation("insert"))])

    if "update" in operations:
        def update_item(item_id: str, payload: update_schema, db: Session = Depends(get_db)):
            return service_factory(db).update(item_id, payload.model_dump(exclude_unset=True, exclude_none=True))
        router.add_api_route("/{item_id}", update_item, methods=["PUT"], response_model=response_schema, dependencies=[Depends(require_operation("update"))])

    if "delete" in operations:
        def clear_items(db: Session = Depends(get_db)):
            return service_factory(db).clear_unused()
        router.add_api_route(
            "/clear",
            clear_items,
            methods=["DELETE"],
            response_model=dict,
            summary="Vaciar registros no relacionados",
            dependencies=[Depends(require_operation("delete"))],
        )

        def delete_item(item_id: str, db: Session = Depends(get_db)):
            service_factory(db).delete(item_id)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        router.add_api_route("/{item_id}", delete_item, methods=["DELETE"], status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_operation("delete"))])
    return router
