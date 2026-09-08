from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from app.config.settings import settings


class Base(DeclarativeBase):
    pass


database_url = settings.resolved_database_url


def create_mysql_database_if_missing(url: str) -> None:
    """Create the configured MySQL database before SQLAlchemy creates its tables."""
    parsed_url = make_url(url)
    database_name = parsed_url.database
    if not database_name:
        raise ValueError("DB_NAME es obligatorio para una conexión MySQL")

    # MySQL identifiers cannot be passed as bound parameters; escaping backticks
    # preserves the configured identifier while preventing identifier injection.
    safe_name = database_name.replace("`", "``")
    # An empty database component renders a server-level MySQL URL (ending in /).
    server_engine = create_engine(parsed_url.set(database=""), connect_args={"charset": "utf8mb4"})
    try:
        with server_engine.begin() as connection:
            connection.execute(text(
                f"CREATE DATABASE IF NOT EXISTS `{safe_name}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci"
            ))
    finally:
        server_engine.dispose()


if database_url.startswith("mysql+"):
    create_mysql_database_if_missing(database_url)

engine_args = (
    {"connect_args": {"check_same_thread": False}}
    if database_url.startswith("sqlite")
    else {"connect_args": {"charset": "utf8mb4"}}
)
engine = create_engine(database_url, **engine_args)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
