from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from sqlalchemy import String, ForeignKey, Date
from .base import Base

class Admin(Base):
    __tablename__ = "admin"

    id_1: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True
    )  # PK et FK vers users
    access_level: Mapped[str] = mapped_column(String(50), nullable=False)
    promotion_date: Mapped[date] = mapped_column(Date, nullable=False)
    id: Mapped[int] = mapped_column(
        ForeignKey("access_level.id"), nullable=False
    )  # FK vers access_level

    # Relations
    user: Mapped["User"] = relationship(back_populates="admin")
    access_level_rel: Mapped["AccessLevel"] = relationship(back_populates="admins")
