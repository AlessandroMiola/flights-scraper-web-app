from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .apis.api import api_router
from .apps.api import app_router
from .core.config import settings


def include_router(app):
    app.include_router(api_router)
    app.include_router(app_router)


def configure_staticfiles(app):
    app.mount("/static", StaticFiles(directory="src/static"), name="static")


app = FastAPI(
    title=settings.PROJECT_TITLE,
    version=settings.PROJECT_VERSION,
)
include_router(app)
configure_staticfiles(app)
