# models/role.py
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Role(Base):
  __tablename__ = "role"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  label: Mapped[str] = mapped_column(nullable=False)

  # Relation
  users: Mapped[List["User"]] = relationship(back_populates="role")
  