from fastapi import FastAPI
from app.config import settings
from app.contexts.users.infrastructure.db import Base, engine
from app.contexts.users.infrastructure import models as users_models
from app.contexts.users.infrastructure.api import router as users_router
from app.contexts.auth.infrastructure.api import router as auth_router


# Crear tablas (init simple; en prod usar Alembic)
Base.metadata.create_all(bind=engine)


app = FastAPI(title=settings.APP_NAME)
app.include_router(users_router, prefix=settings.API_PREFIX)
app.include_router(auth_router, prefix=settings.API_PREFIX)

@app.get("/")
async def root():
    return {"service": settings.APP_NAME, "ok": True}