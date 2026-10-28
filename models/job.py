from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import List
from .base import Base

class Job(Base):
  __tablename__ = "Job"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  label: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

  # Relation
  staff_members: Mapped[List["Staff"]] = relationship(back_populates="job_rel")
