from ..base import Base, TableNameMixin
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional


class Flight(Base, TableNameMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    is_round_trip: Mapped[bool] = mapped_column(Boolean, nullable=False)
    departure_location: Mapped[str] = mapped_column(String, nullable=False)
    arrival_location: Mapped[str] = mapped_column(String, nullable=False)
    departure_location_comeback: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )
    arrival_location_comeback: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )
    departure_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    arrival_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    departure_date_comeback: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )
    arrival_date_comeback: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )
    price: Mapped[float] = mapped_column(Float, nullable=False)
    luggage_type: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )
