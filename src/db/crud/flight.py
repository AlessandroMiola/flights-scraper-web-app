from sqlalchemy.orm import Session

from src.db.models.flight import Flight
from src.db.models.parameter import Parameter
from src.entities.flight import FlightShow


def post_flight_data(
        params: Parameter,
        flight_data: FlightShow,
        db: Session
):
    flight = Flight(parameters=params, **flight_data.model_dump())
    db.add(flight)
    db.commit()
    db.refresh(flight)
    return flight
