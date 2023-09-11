from fastapi import APIRouter

from src.apis.v1 import flights


api_router = APIRouter()
api_router.include_router(flights.router, prefix="/flights", tags=["flights"])
