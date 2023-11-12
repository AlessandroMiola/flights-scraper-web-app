from datetime import date
from typing import Optional

from sqlalchemy import Boolean, Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_class import Base, TableNameMixin


class Parameter(Base, TableNameMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    is_two_way_trip: Mapped[bool] = mapped_column(Boolean, nullable=False)
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
    flights = relationship(
        "Flight",
        back_populates="parameters",
        cascade="all, delete-orphan"
    )
