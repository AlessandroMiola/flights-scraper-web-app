from datetime import datetime
from fastapi import APIRouter
from ...entities.flight import Flight


router = APIRouter()


@router.get("/", response_model=Flight)
async def get_flights():
    return {
        "is_round_trip": False,
        "departure_location": "MIL",
        "arrival_location": "ROM",
        "departure_date": datetime(2023, 1, 1),
        "arrival_date": datetime(2023, 1, 2),
        "price": 23.90,
        "luggage_type": "Borsa piccola",
    }
