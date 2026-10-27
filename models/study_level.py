from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import List
from .base import Base

class StudyLevel(Base):
  __tablename__ = "study_level"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  label: Mapped[str] = mapped_column(String(50), nullable=False)

  # Relation
  students: Mapped[List["Student"]] = relationship(back_populates="study_level")
