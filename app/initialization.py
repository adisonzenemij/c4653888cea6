from pathlib import Path

from sqlalchemy import inspect, select, text
from app.config.database import Base, SessionLocal, engine
from app.models.entities_model import *  # Registers all ORM models in Base.metadata.


SQL_DIRECTORY = Path(__file__).resolve().parent.parent / "sql"
SEED_FILES = (
    "sd_6bb63bb4.sql",
    "ms_8b6bd18a.sql",
    "ms_2e794a8f.sql",
    "tg_9a7bbe6f.sql",
    "tg_8a2579bf.sql",
    "tg_2f997592.sql",
    "sd_1a9ea48c.sql",
    "sd_3a731d00.sql",
    "tg_5c72c20c.sql",
    "tg_8a26b478.sql",
    "pm_8e417bb2.sql",
    "pm_0d3dc00e.sql",
)


def _execute_seed_file(filename: str) -> None:
    content = (SQL_DIRECTORY / filename).read_text(encoding="utf-8")
    with engine.begin() as connection:
        for statement in (value.strip() for value in content.split(";")):
            if statement:
                connection.exec_driver_sql(statement)


def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    resource_table = Ms2e794a8fModel.__tablename__
    for index in inspector.get_indexes(resource_table):
        if index.get("unique") and index.get("column_names") == ["fd_entity"]:
            with engine.begin() as connection:
                connection.execute(text(f"ALTER TABLE `{resource_table}` DROP INDEX `{index['name']}`"))
    user_table = Tg5c72c20cModel.__tablename__
    if "tg_9a7bbe6f" not in {column["name"] for column in inspector.get_columns(user_table)}:
        with engine.begin() as connection:
            connection.execute(text(f"ALTER TABLE `{user_table}` ADD COLUMN tg_9a7bbe6f VARCHAR(36) NULL"))
    role_table = Tg9a7bbe6fModel.__tablename__
    role_foreign_key = "fk_tg_a814_b7308901c01f_role_data"
    has_role_relation = any(
        foreign_key.get("constrained_columns") == ["tg_9a7bbe6f"]
        and foreign_key.get("referred_table") == role_table
        for foreign_key in inspect(engine).get_foreign_keys(user_table)
    )
    if not has_role_relation:
        with engine.begin() as connection:
            connection.execute(text(
                f"ALTER TABLE `{user_table}` ADD CONSTRAINT `{role_foreign_key}` "
                f"FOREIGN KEY (`tg_9a7bbe6f`) REFERENCES `{role_table}` (`id_universal`)"
            ))
    for filename in SEED_FILES:
        _execute_seed_file(filename)


def cors_origins() -> list[str]:
    with SessionLocal() as db:
        return list(db.scalars(select(Sd1a9ea48cModel.fd_service)))
