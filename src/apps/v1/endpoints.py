from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Form, Request, responses, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.db.crud.parameter import create_params
from src.db.session import get_db
from src.entities.flight import FlightCreate


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
    is_round_trip: bool = Form(...),
    departure_location: str = Form(...),
    arrival_location: str = Form(...),
    departure_date: date = Form(...),
    departure_location_comeback: Optional[str] = Form(None),
    arrival_location_comeback: Optional[str] = Form(None),
    departure_date_comeback: date = Form(None),
    db: Session = Depends(get_db)
):
    flight = FlightCreate(
        is_round_trip=is_round_trip,
        departure_location=departure_location,
        arrival_location=arrival_location,
        departure_date=departure_date,
        departure_location_comeback=departure_location_comeback,
        arrival_location_comeback=arrival_location_comeback,
        departure_date_comeback=departure_date_comeback
    )
    params = create_params(flight=flight, db=db)
    scraped_data = "default"
    return responses.RedirectResponse(
        url="/",
        status_code=status.HTTP_302_FOUND
    )
