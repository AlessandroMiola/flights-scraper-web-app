from sqlalchemy.orm import Session

from src.db.models.flight import Flight
from src.entities.flight import FlightShow


def post_flight_data(flight_data: FlightShow, db: Session):
    flight = Flight(
        is_two_way_trip=flight_data.is_two_way_trip,
        departure_location=flight_data.departure_location,
        arrival_location=flight_data.arrival_location,
        departure_location_comeback=flight_data.departure_location_comeback,
        arrival_location_comeback=flight_data.arrival_location_comeback,
        departure_date=flight_data.departure_date,
        arrival_date=flight_data.arrival_date,
        departure_date_comeback=flight_data.departure_date_comeback,
        arrival_date_comeback=flight_data.arrival_date_comeback,
        airline=flight_data.airline,
        airline_comeback=flight_data.airline_comeback,
        flight_length=flight_data.flight_length,
        flight_length_comeback=flight_data.flight_length_comeback,
        trip_type=flight_data.trip_type,
        trip_type_comeback=flight_data.trip_type_comeback,
        price=flight_data.price,
        currency=flight_data.currency,
        luggage_type=flight_data.luggage_type,
        luggage_type_comeback=flight_data.luggage_type_comeback
    )
    db.add(flight)
    db.commit()
    db.refresh(flight)
    return flight
