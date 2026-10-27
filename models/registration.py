from datetime import date
from typing import Optional
from sqlalchemy import Boolean, Date, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Registration(Base):
  __tablename__ = "registrations"

  id: Mapped[str] = mapped_column(String(50), primary_key=True)
  register_date: Mapped[date] = mapped_column(Date, nullable=False)
  presence: Mapped[Optional[bool]] = mapped_column(Boolean)
  status: Mapped[str] = mapped_column(
      Enum(
          "ENREGISTRE",
          "DESCRIPTION",
          "EN_ATTENTE",
          name="registration_status_enum",
      ),
      nullable=False,
  )
  id_1: Mapped[int] = mapped_column(
      ForeignKey("students.id_1"), nullable=False
  )  # FK vers students
  id_2: Mapped[int] = mapped_column(
      ForeignKey("session.id"), nullable=False
  )  # FK vers session

  # Relations
  student: Mapped["Student"] = relationship(back_populates="registrations")
  session: Mapped["Session"] = relationship(back_populates="registrations")