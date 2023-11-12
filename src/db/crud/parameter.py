from sqlalchemy.orm import Session

from src.db.models.parameter import Parameter
from src.entities.flight import FlightCreate


def create_params(flight: FlightCreate, db: Session):
    params = Parameter(**flight.model_dump())
    db.add(params)
    db.commit()
    db.refresh(params)
    return params


def delete_params_by_id(id: int, db: Session):
    param_in_db = db.query(Parameter).filter(Parameter.id == id)
    if not param_in_db.first():
        return {"error": f"Could not find parameters with id {id}."}
    param_in_db.delete()
    db.commit()
    return {"msg": f"Deleted parameters with id {id}."}
