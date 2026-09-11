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
    "tg_2f997592.sql",
    "tg_8a2579bf.sql",
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
    role_permit_table = Tg8a26b478Model.__tablename__
    permit_columns = {column["name"] for column in inspect(engine).get_columns(role_permit_table)}
    for column in ("sd_insert", "sd_update", "sd_delete"):
        if column not in permit_columns:
            with engine.begin() as connection:
                connection.execute(text(f"ALTER TABLE `{role_permit_table}` ADD COLUMN `{column}` VARCHAR(36) NULL"))
    for filename in SEED_FILES:
        _execute_seed_file(filename)
    with engine.begin() as connection:
        for column in ("sd_insert", "sd_update", "sd_delete"):
            connection.execute(text(
                f"UPDATE `{role_permit_table}` SET `{column}` = 'ecbec726-d783-4021-8b10-3dd4e9b1d2c4' "
                f"WHERE `{column}` IS NULL"
            ))
    access_table = Tg2f997592Model.__tablename__
    existing_permit_relations = {
        foreign_key["constrained_columns"][0]
        for foreign_key in inspect(engine).get_foreign_keys(role_permit_table)
        if len(foreign_key.get("constrained_columns", [])) == 1
        and foreign_key.get("referred_table") == access_table
    }
    for column in ("sd_insert", "sd_update", "sd_delete"):
        if column not in existing_permit_relations:
            with engine.begin() as connection:
                connection.execute(text(
                    f"ALTER TABLE `{role_permit_table}` ADD CONSTRAINT `fk_{role_permit_table}_{column}` "
                    f"FOREIGN KEY (`{column}`) REFERENCES `{access_table}` (`id_universal`)"
                ))
    # Roles created before Roles Módulos existed receive the same safe default.
    with SessionLocal() as db:
        denied = db.scalar(select(Tg2f997592Model).where(Tg2f997592Model.fd_name == "Denegado"))
        if denied:
            modules = list(db.scalars(select(Ms8b6bd18aModel)))
            for role in db.scalars(select(Tg9a7bbe6fModel)):
                current = set(db.scalars(select(Tg8a2579bfModel.ms_8b6bd18a).where(Tg8a2579bfModel.tg_9a7bbe6f == role.id_universal)))
                for module in modules:
                    if module.id_universal not in current:
                        db.add(Tg8a2579bfModel(ms_8b6bd18a=module.id_universal, tg_2f997592=denied.id_universal, tg_9a7bbe6f=role.id_universal))
            db.commit()


def cors_origins() -> list[str]:
    with SessionLocal() as db:
        return list(db.scalars(select(Sd1a9ea48cModel.fd_service)))
