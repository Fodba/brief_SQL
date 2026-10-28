from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from sqlalchemy import (
    Date,
    ForeignKey,
    String,
    Text,
    Enum,
)
from typing import List, Optional
from .base import Base

class Session(Base):
    __tablename__ = "session"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(
        Enum("OUVERT", "FERMÉ", "ARCHIVÉ", name="session_status_enum"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    max_capacity: Mapped[int] = mapped_column(nullable=False)
    prerequisite: Mapped[Optional[str]] = mapped_column(Text)
    id_1: Mapped[str] = mapped_column(
        ForeignKey("classroom.id"), nullable=False
    )  # FK vers classroom
    id_2: Mapped[int] = mapped_column(
        ForeignKey("teachers.id"), nullable=False
    )  # FK vers teachers

    # Relations
    classroom: Mapped["Classroom"] = relationship(back_populates="sessions")
    teacher: Mapped["Teacher"] = relationship(back_populates="sessions")
    registrations: Mapped[List["Registration"]] = relationship(
        back_populates="session"
    )
