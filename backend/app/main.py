from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.users import router as users_routes
from app.database.db import create_db_and_tables

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users_routes, prefix="/api", tags=["users"])
