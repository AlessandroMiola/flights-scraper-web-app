from fastapi import APIRouter
from .v1 import render_templates


app_router = APIRouter()
app_router.include_router(render_templates.router, include_in_schema=False)
