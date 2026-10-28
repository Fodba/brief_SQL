from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from sqlalchemy import Date, ForeignKey, String
from typing import List
from .base import Base


class Student(Base):
    __tablename__ = "students"

    id_1: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True
    )  # PK et FK vers users
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    phone: Mapped[str] = mapped_column(String(50))
    obtained_certification: Mapped[str] = mapped_column(String(50))
    registration_date: Mapped[date] = mapped_column(Date, nullable=False)
    id: Mapped[int] = mapped_column(
        ForeignKey("study_level.id"), nullable=False
    )  # FK vers study_level

    # Relations
    user: Mapped["User"] = relationship(back_populates="student")
    study_level: Mapped["StudyLevel"] = relationship(back_populates="students")
    registrations: Mapped[List["Registration"]] = relationship(
        back_populates="student"
    )
