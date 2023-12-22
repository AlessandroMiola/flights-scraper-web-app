from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles

from src.apis.api import api_router
from src.core.config import settings
from src.dashboard.app import app as dash_app


def include_router(app):
    app.include_router(api_router)


def configure_staticfiles(app):
    app.mount("/static", StaticFiles(directory="src/static"), name="static")


def configure_dash_app(app, dash_app):
    app.mount("/price-history", WSGIMiddleware(dash_app.server))


app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)
include_router(app)
configure_staticfiles(app)
configure_dash_app(app, dash_app)
