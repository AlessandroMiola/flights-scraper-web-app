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
    trip_type: str = Form(...),
    departure_location: str = Form(...),
    arrival_location: str = Form(...),
    # departure_location_comeback: Optional[str] = Form(),
    # arrival_location_comeback: Optional[str] = Form(),
):
    print(f"Trip type is {trip_type}")
    print(f"Departure from {departure_location}")
    print(f"Arrival to {arrival_location}")
    # print(f"Departure (comeback) from {departure_location_comeback}")
    # print(f"Arrival (comeback) to {arrival_location_comeback}")
