from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from .base import Base


class AccessLevel(Base):
    __tablename__ = "access_level"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    label: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    # Relation
    admins: Mapped[List["Admin"]] = relationship(
        back_populates="access_level_rel"
    )
