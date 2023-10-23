from sqlalchemy.orm import Session

from src.db.models.parameter import Parameter
from src.entities.flight import FlightCreate


def create_params(flight: FlightCreate, db: Session):
    params = Parameter(**flight.model_dump())
    db.add(params)
    db.commit()
    db.refresh(params)
    return params
