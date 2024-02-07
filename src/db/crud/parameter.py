from sqlalchemy.orm import Session

from src.db.models.parameter import Parameter
from src.entities.flight import FlightCreate


def create_params(flight: FlightCreate, db: Session):
    params = Parameter(**flight.model_dump())
    db.add(params)
    db.commit()
    db.refresh(params)
    return params


def get_params_by_id(params_id: int, db: Session):
    return db.query(Parameter).filter(Parameter.id == params_id)


def delete_params_by_id(params_id: int, db: Session):
    param_in_db = db.query(Parameter).filter(Parameter.id == params_id)
    if not param_in_db.first():
        return {"error": f"Could not find parameters with id {params_id}."}
    param_in_db.delete()
    db.commit()
    return {"msg": f"Deleted parameters with id {params_id}."}
