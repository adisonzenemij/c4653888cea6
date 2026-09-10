from __future__ import annotations

from typing import Generic, TypeVar
from sqlalchemy import func, select
from sqlalchemy.orm import Session

ModelT = TypeVar("ModelT")

TABLE_LABELS = {
    "sd_a1bb_a6baddf4c35a": "Orígenes CORS",
    "sd_a9da_8e0684f3f419": "Métodos",
    "pm_a0da_73b502c724d5": "Servicios",
    "pm_8f13_174467919cda": "Recursos",
    "pm_b5eb_65d1aeb635fc": "Sociedades",
    "tg_a814_b7308901c01f": "Usuarios",
    "pm_ac73_a0c3754a0c60": "Anónimos",
    "pm_bfe4_0a191a6f082d": "Alcances",
    "pm_a9e4_1879447f9657": "Tipos",
    "pm_a98d_4efe1131fd87": "Encuestas",
    "pm_898e_48db3e1fb7b8": "Preguntas",
    "pm_96ee_18d1272728c6": "Valores",
    "pm_9482_b7b3bf232a17": "Respuestas",
}


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
                    label = TABLE_LABELS.get(table.name, table.name)
                    references[label] = references.get(label, 0) + count
        return [
            {"module": module, "records": count}
            for module, count in references.items()
        ]

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
