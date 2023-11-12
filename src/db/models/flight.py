from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_class import Base, TableNameMixin


class Flight(Base, TableNameMixin):
    parameters_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("parameters.id", ondelete="CASCADE"),
        nullable=False
    )
    parameters = relationship(
        "Parameter",
        foreign_keys=[parameters_id],
        back_populates="flights",
        cascade="all",
    )
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
    airline: Mapped[str] = mapped_column(String, nullable=False)
    airline_comeback: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True
    )
    flight_length: Mapped[str] = mapped_column(String, nullable=False)
    flight_length_comeback: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True
    )
    trip_type: Mapped[str] = mapped_column(String, nullable=False)
    trip_type_comeback: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True
    )
    price: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    luggage_type: Mapped[str] = mapped_column(String, nullable=False)
    luggage_type_comeback: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )
