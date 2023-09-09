from ..base import Base, TableNameMixin
from datetime import date
from sqlalchemy import Boolean, Date, String
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional


class Parameter(Base, TableNameMixin):
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
    departure_date: Mapped[date] = mapped_column(Date, nullable=False)
    departure_date_comeback: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )
