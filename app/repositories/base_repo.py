from __future__ import annotations

from typing import Generic, TypeVar
from sqlalchemy import func, select
from sqlalchemy.orm import Session

ModelT = TypeVar("ModelT")


class BaseRepository(Generic[ModelT]):
    def __init__(self, db: Session, model: type[ModelT]):
        self.db, self.model = db, model

    def list(self) -> list[ModelT]:
        return list(self.db.scalars(select(self.model)))

    def page(self, offset: int = 0, limit: int = 25) -> tuple[list[ModelT], int]:
        items = list(self.db.scalars(select(self.model).offset(offset).limit(limit)))
        total = self.db.scalar(select(func.count()).select_from(self.model)) or 0
        return items, total

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

    def clear_unused(self) -> dict[str, int]:
        """Remove rows only when no other mapped table references them."""
        target_table = self.model.__table__
        inbound_keys = [
            foreign_key
            for table in target_table.metadata.tables.values()
            for foreign_key in table.foreign_keys
            if foreign_key.column.table is target_table
        ]
        deleted = 0
        preserved = 0

        for item in self.list():
            is_referenced = any(
                self.db.scalar(
                    select(func.count())
                    .select_from(foreign_key.parent.table)
                    .where(
                        foreign_key.parent
                        == getattr(item, foreign_key.column.key)
                    )
                )
                for foreign_key in inbound_keys
            )
            if is_referenced:
                preserved += 1
                continue
            self.db.delete(item)
            deleted += 1

        self.db.commit()
        return {"deleted": deleted, "preserved": preserved}
