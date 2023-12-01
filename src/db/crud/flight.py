from itertools import groupby

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


def get_all_flights_data(db: Session):
    all_flights = db.query(Flight).all()
    all_flights.sort(key=lambda flight: flight.parameters_id)
    grouped_flights = {
        id: list(group) for id, group in groupby(
            all_flights, key=lambda flight: flight.parameters_id
        )
    }
    return grouped_flights


def get_flight_data_by_id(id: int, db: Session):
    return db.query(Flight).filter(Flight.parameters_id == id)


def update_flight_data_by_id(
    id: int,
    new_flight_data: list[FlightShow],
    db: Session
):
    updated_flights = []
    for new_flight in new_flight_data:
        updated_flight = Flight(parameters_id=id, **new_flight.model_dump())
        db.add(updated_flight)
        updated_flights.append(updated_flight)
    db.commit()
    return updated_flights


def delete_flight_data_by_id(id: int, db: Session):
    flights_in_db = get_flight_data_by_id(id=id, db=db).all()
    if not flights_in_db:
        return {"error": f"Could not find flights having parameters_id {id}."}
    flights_in_db.delete()
    db.commit()
    return {"msg": f"Deleted flights having parameters_id {id}."}
