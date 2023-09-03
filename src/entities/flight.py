from datetime import datetime
from pydantic import BaseModel, model_validator
from typing import Any, Optional


class Flight(BaseModel):
    is_round_trip: bool
    departure_location: str
    arrival_location: str
    departure_location_comeback: Optional[str] = None
    arrival_location_comeback: Optional[str] = None
    departure_date: datetime
    arrival_date: datetime
    departure_date_comeback: Optional[datetime] = None
    arrival_date_comeback: Optional[datetime] = None
    price: float
    luggage_type: str

    @model_validator(mode="before")
    @classmethod
    def validate_round_trip_attributes(cls, v: dict[str, Any]):
        if v["is_round_trip"]:
            assert v["departure_location_comeback"] is not None
            assert v["arrival_location_comeback"] is not None
            assert v["departure_date_comeback"] is not None
            assert v["arrival_date_comeback"] is not None
        return v

    @model_validator(mode="before")
    @classmethod
    def validate_arrival_dates(cls, v: dict[str, Any]):
        assert v["departure_date"] < v["arrival_date"]
        if "departure_date_comeback" in v:
            assert v["departure_date_comeback"] < v["arrival_date_comeback"]
        return v
