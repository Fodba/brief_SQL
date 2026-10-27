# models/user.py
from datetime import date
from typing import Optional
from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lastname: Mapped[str] = mapped_column(nullable=False)
    firstname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    creation_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False)
    id_1: Mapped[int] = mapped_column(ForeignKey("role.id"), nullable=False)

    # Relations
    role: Mapped["Role"] = relationship(back_populates="users")
    student: Mapped[Optional["Student"]] = relationship(
        back_populates="user", uselist=False
    )
    teacher: Mapped[Optional["Teacher"]] = relationship(
        back_populates="user", uselist=False
    )
    staff: Mapped[Optional["Staff"]] = relationship(
        back_populates="user", uselist=False
    )
    admin: Mapped[Optional["Admin"]] = relationship(
        back_populates="user", uselist=False
    )
    