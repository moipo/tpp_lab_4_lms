import os

from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker

# DATABASE_URL can be overridden (e.g. by tests) via environment variable.
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./db.sqlite3")

# SQLite in Python is single-threaded by default; disable that check for FastAPI.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# IMPORTANT: SQLite does NOT enforce foreign keys unless this pragma is set
# for every new connection. Without it, cascade deletes would fail / be ignored.
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    # Import models so they are registered on Base before create_all.
    import app.models  # noqa: F401
    Base.metadata.create_all(bind=engine)
