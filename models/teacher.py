from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from sqlalchemy import (
    Date,
    ForeignKey,
    String,
    Numeric,
    Text,
)
from typing import List, Optional
from .base import Base

class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True
    )  # PK et FK vers users
    specialty: Mapped[str] = mapped_column(String(50), nullable=False)
    hire_date: Mapped[Optional[date]] = mapped_column(Date, nullable=False)
    hourly_rate: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    biography: Mapped[Optional[str]] = mapped_column(Text)

    # Relations
    user: Mapped["User"] = relationship(back_populates="teacher")
    sessions: Mapped[List["Session"]] = relationship(back_populates="teacher")
