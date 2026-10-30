from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app import routes
from app.seed import seed_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables (if missing) and seed sample data on first launch.
    init_db()
    seed_data()
    yield


app = FastAPI(title="LMS API", lifespan=lifespan)
app.include_router(routes.router)


@app.get("/")
def root():
    return {"status": "ok"}
