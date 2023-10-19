from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.apis.api import api_router
from src.core.config import settings


def include_router(app):
    app.include_router(api_router)


def configure_staticfiles(app):
    app.mount("/static", StaticFiles(directory="src/static"), name="static")


app = FastAPI(
    title=settings.PROJECT_TITLE,
    version=settings.PROJECT_VERSION,
)
include_router(app)
configure_staticfiles(app)
