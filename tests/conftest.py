import os

# Use a throwaway database for the test session so we never touch the
# committed db.sqlite3 that ships with the project.
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client():
    if os.path.exists("test.db"):
        os.remove("test.db")
    # The app lifespan (startup) creates tables and seeds the test DB.
    with TestClient(app) as c:
        yield c
    if os.path.exists("test.db"):
        os.remove("test.db")
