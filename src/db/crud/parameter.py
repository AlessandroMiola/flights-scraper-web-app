from sqlalchemy.orm import Session

from src.db.models.parameter import Parameter
from src.entities.flight import FlightCreate


def create_params(flight: FlightCreate, db: Session):
    params = Parameter(
        is_round_trip=flight.is_round_trip,
        departure_location=flight.departure_location,
        arrival_location=flight.arrival_location,
        departure_location_comeback=flight.departure_location_comeback,
        arrival_location_comeback=flight.arrival_location_comeback,
        departure_date=flight.departure_date,
        departure_date_comeback=flight.departure_date_comeback
    )
    db.add(params)
    db.commit()
    db.refresh(params)
    return params
