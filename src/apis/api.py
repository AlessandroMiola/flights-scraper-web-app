from fastapi import APIRouter

from src.apis.v1 import endpoints


api_router = APIRouter()
api_router.include_router(endpoints.router, include_in_schema=False)
