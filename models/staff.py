from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from sqlalchemy import String, ForeignKey, Date, Text
from .base import Base

class Staff(Base):
    __tablename__ = "Staff"

    id_1: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True
    )  # PK et FK vers users
    job: Mapped[str] = mapped_column(String(50), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    responsabilities: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(
        ForeignKey("Job.id"), nullable=False
    )  # FK vers Job

    # Relations
    user: Mapped["User"] = relationship(back_populates="staff")
    job_rel: Mapped["Job"] = relationship(back_populates="staff_members")
