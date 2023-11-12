import json
from datetime import date
from typing import Optional

from fastapi import (
    APIRouter, Depends, Form, HTTPException, Request, responses, status
)
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy.orm import Session

from src.core.scraper.scraper import scrape_data
from src.db.crud.flight import (
    delete_flight_data_by_id,
    get_all_flights_data,
    get_flight_data_by_id,
    post_flight_data
)
from src.db.crud.parameter import create_params, delete_params_by_id
from src.db.session import get_db
from src.entities.flight import FlightCreate, FlightShow


templates = Jinja2Templates(directory="src/templates")
router = APIRouter()


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        name="flight-details/home.html",
        context={"request": request},
    )


@router.post("/")
def update_params_and_call_scraper(
    request: Request,
    is_two_way_trip: bool = Form(...),
    departure_location: str = Form(...),
    arrival_location: str = Form(...),
    departure_date: date = Form(...),
    departure_location_comeback: Optional[str] = Form(None),
    arrival_location_comeback: Optional[str] = Form(None),
    departure_date_comeback: Optional[date] = Form(None),
    db: Session = Depends(get_db)
):
    exceptions = []
    try:
        flight = FlightCreate(
            is_two_way_trip=is_two_way_trip,
            departure_location=departure_location,
            arrival_location=arrival_location,
            departure_date=departure_date,
            departure_location_comeback=departure_location_comeback,
            arrival_location_comeback=arrival_location_comeback,
            departure_date_comeback=departure_date_comeback
        )
        parameters = create_params(flight=flight, db=db)
        scraped_flight_data = scrape_data(
            is_two_way_trip=flight.is_two_way_trip,
            departure_location=flight.departure_location,
            arrival_location=flight.arrival_location,
            departure_date=flight.departure_date,
            departure_location_comeback=flight.departure_location_comeback,
            arrival_location_comeback=flight.arrival_location_comeback,
            departure_date_comeback=flight.departure_date_comeback
        )
        for data in scraped_flight_data:
            flight_data_out = FlightShow(**data)
            _ = post_flight_data(
                    params=parameters, flight_data=flight_data_out, db=db
                )
        return responses.RedirectResponse(
            url="/",
            status_code=status.HTTP_302_FOUND
        )
    except ValidationError as e:
        exceptions_list = json.loads(e.json())
        for item in exceptions_list:
            exceptions.append(item.get("loc")[-1] + ": " + item.get("msg"))
        return templates.TemplateResponse(
            name="flight-details/home.html",
            context={
                "request": request,
                "exceptions": exceptions
            }
        )


@router.get(
    "/all-flights",
    response_model=dict[int, list[FlightShow]],
    status_code=status.HTTP_200_OK
)
def get_all_flights_details(db: Session = Depends(get_db)):
    all_flights_data = get_all_flights_data(db=db)
    if not all_flights_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No flight data available."
        )
    return all_flights_data


@router.get(
    "/flight/{id}",
    response_model=list[FlightShow],
    status_code=status.HTTP_200_OK
)
def get_flight_details(id: int, db: Session = Depends(get_db)):
    flight_data = get_flight_data_by_id(id=id, db=db)
    if not flight_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No flight data available for id {id}."
        )
    return flight_data


@router.delete("/cleanup/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_flight_details(id: int, db: Session = Depends(get_db)):
    msg = delete_flight_data_by_id(id=id, db=db)
    if msg.get("error"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg.get("error")
        )
    _ = delete_params_by_id(id=id, db=db)
    return {"msg": msg.get("msg")}
