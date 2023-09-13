from fastapi import APIRouter

from src.apps.v1 import endpoints


app_router = APIRouter()
app_router.include_router(endpoints.router, include_in_schema=False)
