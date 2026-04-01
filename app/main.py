from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.router_auth import router as auth_router
from app.router_places import router as places_router
from app.router_projects import router as projects_router
from core.cfg import settings
from database.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    import models.models  
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title=settings.APP_TITLE, version="1.0.0", lifespan=lifespan)
app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(places_router)
