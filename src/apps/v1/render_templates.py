from datetime import date
from typing import Optional
from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="src/templates")
router = APIRouter()


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        name="flight-details/home.html",
        context={"request": request},
    )


@router.post("/")
def func_name(
    request: Request,
    is_round_trip: bool = Form(...),
    departure_location: str = Form(...),
    arrival_location: str = Form(...),
    departure_date: date = Form(...),
    departure_location_comeback: Optional[str] = Form(None),
    arrival_location_comeback: Optional[str] = Form(None),
    departure_date_comeback: date = Form(None)
):
    print(f"Trip type is {is_round_trip}")
    print(f"Departure from {departure_location}")
    print(f"Arrival to {arrival_location}")
    print(f"Departure on {departure_date}")
    print(f"Departure (comeback) from {departure_location_comeback}")
    print(f"Arrival (comeback) to {arrival_location_comeback}")
    print(f"Departure (comeback) on {departure_date_comeback}")
