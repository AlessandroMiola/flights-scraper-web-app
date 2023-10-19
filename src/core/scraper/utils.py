from datetime import (
    date, datetime, time as datetime_time, timedelta
)


def add_n_days_to_input_dates(date: date, n_days: int):
    return date + timedelta(n_days)


def combine_input_dates_and_scraped_timestr(date: date, time_str: str):
    return datetime.combine(date, datetime_time.fromisoformat(time_str))
