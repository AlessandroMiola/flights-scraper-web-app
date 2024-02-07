from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, model_validator


class FlightBase(BaseModel):
    is_two_way_trip: bool
    departure_location: str
    arrival_location: str
    departure_location_comeback: str | None = None
    arrival_location_comeback: str | None = None
    departure_date: datetime
    departure_date_comeback: datetime | None = None


class FlightCreate(FlightBase):
    pass

    @model_validator(mode="before")
    @classmethod
    def validate_two_way_trip_attributes(cls, v: Any):
        if isinstance(v, dict):
            if v["is_two_way_trip"]:
                assert v["departure_location_comeback"] is not None
                assert v["arrival_location_comeback"] is not None
                assert v["departure_date_comeback"] is not None
        else:
            if v.is_two_way_trip:
                assert v.departure_location_comeback is not None
                assert v.arrival_location_comeback is not None
                assert v.departure_date_comeback is not None
        return v

    @model_validator(mode="before")
    @classmethod
    def validate_input_dates(cls, v: Any):
        if isinstance(v, dict):
            assert v["departure_date"] >= date.today()
            if "departure_date_comeback" in v and v["departure_date_comeback"] is not None:
                assert v["departure_date"] < v["departure_date_comeback"]
        else:
            assert v.departure_date >= date.today()
            if v.departure_date_comeback is not None:
                assert v.departure_date < v.departure_date_comeback
        return v


class FlightShow(FlightBase):
    arrival_date: datetime
    arrival_date_comeback: datetime | None = None
    airline: str
    airline_comeback: str | None = None
    flight_length: str
    flight_length_comeback: str | None = None
    trip_type: str
    trip_type_comeback: str | None = None
    price: float
    currency: str
    luggage_type: str
    luggage_type_comeback: str | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_arrival_dates(cls, v: Any):
        if isinstance(v, dict):
            assert v["departure_date"] < v["arrival_date"]
            if "departure_date_comeback" in v and v["departure_date_comeback"] is not None:
                assert v["departure_date_comeback"] < v["arrival_date_comeback"]
        else:
            assert v.departure_date < v.arrival_date
            if v.departure_date_comeback is not None:
                assert v.departure_date_comeback < v.arrival_date_comeback
        return v
