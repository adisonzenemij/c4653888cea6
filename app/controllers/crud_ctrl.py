from typing import Callable
from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.dependencies.dependencies import get_current_user


def create_crud_router(
    prefix: str, tags: list[str], service_factory: Callable, create_schema: type[BaseModel],
    update_schema: type[BaseModel], response_schema: type[BaseModel], operations: set[str] | None = None,
) -> APIRouter:
    """Creates the HTTP controller; business logic remains in its service."""
    operations = operations or {"list", "page", "create", "update", "delete"}
    router = APIRouter(prefix=prefix, tags=tags, dependencies=[Depends(get_current_user)])

    if "list" in operations:
        def list_items(db: Session = Depends(get_db)):
            return service_factory(db).list()
        router.add_api_route("/", list_items, methods=["GET"], response_model=list[response_schema], summary="Select normal")

    if "page" in operations:
        def page_items(offset: int = Query(0, ge=0), limit: int = Query(25, ge=1, le=100), db: Session = Depends(get_db)):
            items, total = service_factory(db).page(offset, limit)
            return {"offset": offset, "limit": limit, "total": total, "items": items}
        router.add_api_route("/page", page_items, methods=["GET"], response_model=dict, summary="Select paginado")

    if "create" in operations:
        def create_item(payload: create_schema, db: Session = Depends(get_db)):
            return service_factory(db).create(payload.model_dump())
        router.add_api_route("/", create_item, methods=["POST"], response_model=response_schema, status_code=status.HTTP_201_CREATED)

    if "update" in operations:
        def update_item(item_id: str, payload: update_schema, db: Session = Depends(get_db)):
            return service_factory(db).update(item_id, payload.model_dump(exclude_unset=True, exclude_none=True))
        router.add_api_route("/{item_id}", update_item, methods=["PUT"], response_model=response_schema)

    if "delete" in operations:
        def delete_item(item_id: str, db: Session = Depends(get_db)):
            service_factory(db).delete(item_id)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        router.add_api_route("/{item_id}", delete_item, methods=["DELETE"], status_code=status.HTTP_204_NO_CONTENT)
    return router
