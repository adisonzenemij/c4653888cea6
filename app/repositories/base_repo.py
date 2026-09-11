from __future__ import annotations

from typing import Generic, TypeVar
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.entities_model import Ms2e794a8fModel

ModelT = TypeVar("ModelT")

class BaseRepository(Generic[ModelT]):
    def __init__(self, db: Session, model: type[ModelT]):
        self.db, self.model = db, model

    def list(self) -> list[ModelT]:
        return self._with_associated(list(self.db.scalars(select(self.model))))

    def page(self, offset: int = 0, limit: int = 25) -> tuple[list[ModelT], int]:
        items = list(self.db.scalars(select(self.model).offset(offset).limit(limit)))
        total = self.db.scalar(select(func.count()).select_from(self.model)) or 0
        return self._with_associated(items), total

    def _with_associated(self, items: list[ModelT]) -> list[ModelT]:
        """Attach inbound-relation details used by the generic CRUD tables."""
        for item in items:
            details = self.referencing_modules(item)
            item.fd_associated = bool(details)
            item.fd_association_details = details
        return items

    def get(self, item_id: str) -> ModelT | None:
        return self.db.get(self.model, item_id)

    def create(self, values: dict) -> ModelT:
        item = self.model(**values)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item: ModelT, values: dict) -> ModelT:
        for key, value in values.items():
            setattr(item, key, value)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: ModelT) -> None:
        self.db.delete(item)
        self.db.commit()

    def referencing_modules(self, item: ModelT) -> list[dict[str, int | str]]:
        """Return modules and record counts that currently reference *item*."""
        target_table = self.model.__table__
        references: dict[str, int] = {}
        for table in target_table.metadata.tables.values():
            for foreign_key in table.foreign_keys:
                if foreign_key.column.table is not target_table:
                    continue
                count = self.db.scalar(
                    select(func.count())
                    .select_from(table)
                    .where(
                        foreign_key.parent
                        == getattr(item, foreign_key.column.key)
                    )
                ) or 0
                if count:
                    references[table.name] = references.get(table.name, 0) + int(count)
        resource_names = self._resource_names_by_table()
        return [
            {
                # ``module`` is retained for the delete-conflict API.
                "module": resource_names.get(table_name, table_name),
                "resource": resource_names.get(table_name, table_name),
                "records": count,
            }
            for table_name, count in references.items()
        ]

    def _resource_names_by_table(self) -> dict[str, str]:
        names: dict[str, str] = {}
        resources = self.db.execute(select(
            Ms2e794a8fModel.id_universal,
            Ms2e794a8fModel.fd_entity,
            Ms2e794a8fModel.fd_name,
        ))
        for resource in resources:
            uuid_parts = resource.id_universal.split("-")
            prefix = resource.fd_entity.split("_", 1)[0]
            if len(uuid_parts) == 5 and prefix:
                names[f"{prefix}_{uuid_parts[-2]}_{uuid_parts[-1]}"] = resource.fd_name
        return names

    def clear_unused(self) -> dict[str, int]:
        """Remove rows only when no other mapped table references them."""
        deleted = 0
        preserved = 0

        for item in self.list():
            if self.referencing_modules(item):
                preserved += 1
                continue
            self.db.delete(item)
            deleted += 1

        self.db.commit()
        return {"deleted": deleted, "preserved": preserved}
