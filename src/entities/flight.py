from typing import Any, Optional

from datetime import date, datetime
from pydantic import BaseModel, model_validator


class FlightBase(BaseModel):
    is_round_trip: bool
    departure_location: str
    arrival_location: str
    departure_location_comeback: Optional[str] = None
    arrival_location_comeback: Optional[str] = None
    departure_date: datetime
    departure_date_comeback: Optional[datetime] = None


class FlightCreate(FlightBase):
    pass

    @model_validator(mode="before")
    @classmethod
    def validate_round_trip_attributes(cls, v: dict[str, Any]):
        if v["is_round_trip"]:
            assert v["departure_location_comeback"] is not None
            assert v["arrival_location_comeback"] is not None
            assert v["departure_date_comeback"] is not None
        return v

    @model_validator(mode="before")
    @classmethod
    def validate_input_dates(cls, v: dict[str, Any]):
        assert v["departure_date"] >= date.today()
        if v["departure_date_comeback"] is not None:
            assert v["departure_date"] < v["departure_date_comeback"]
        return v


class FlightShow(FlightBase):
    arrival_date: datetime
    arrival_date_comeback: Optional[datetime] = None
    price: float
    luggage_type: str

    @model_validator(mode="before")
    @classmethod
    def validate_arrival_dates(cls, v: dict[str, Any]):
        assert v["departure_date"] < v["arrival_date"]
        if v["departure_date_comeback"] is not None:
            assert v["departure_date_comeback"] < v["arrival_date_comeback"]
        return v
