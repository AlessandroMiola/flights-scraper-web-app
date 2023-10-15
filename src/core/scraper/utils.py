import time as system_time

from datetime import (
    date, datetime, time as datetime_time, timedelta
)
from typing import Optional

from src.core.scraper import EdreamsScraper


def add_n_days_to_input_dates(date: date, n_days: int):
    return date + timedelta(n_days)


def combine_input_dates_and_scraped_timestr(date: date, time_str: str):
    return datetime.combine(date, datetime_time.fromisoformat(time_str))


def scrape_data(
    is_two_way_trip: bool,
    departure_location: str,
    arrival_location: str,
    departure_date: date,
    departure_location_comeback: Optional[str] = None,
    arrival_location_comeback: Optional[str] = None,
    departure_date_comeback: Optional[date] = None
):
    scraper = EdreamsScraper()
    scraper.search_flights(
        is_two_way_trip,
        departure_location,
        arrival_location,
        departure_date,
        departure_location_comeback,
        arrival_location_comeback,
        departure_date_comeback
    )
    system_time.sleep(3)
    data = scraper.scrape_flight_data(
        is_two_way_trip,
        departure_date,
        departure_date_comeback
    )
    scraper.close()
    return data
