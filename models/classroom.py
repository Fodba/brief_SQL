from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Text
from typing import List
from .base import Base

class Classroom(Base):
  __tablename__ = "classroom"

  id: Mapped[str] = mapped_column(String(50), primary_key=True)
  name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
  capacity: Mapped[int] = mapped_column(nullable=False)
  location: Mapped[str] = mapped_column(String(50), nullable=False)
  is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
  equipments: Mapped[str] = mapped_column(Text, nullable=False)

  # Relation
  sessions: Mapped[List["Session"]] = relationship(back_populates="classroom")
