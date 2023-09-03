from fastapi import FastAPI
from .apis.api import api_router
from .core.config import settings


app = FastAPI(
    title=settings.PROJECT_TITLE,
    version=settings.PROJECT_VERSION,
)
app.include_router(api_router)
