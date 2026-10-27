from datetime import date
from typing import List, Optional
from sqlalchemy import (
    Boolean,
    Date,
    Enum,
    ForeignKey,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
  pass


class Role(Base):
  __tablename__ = "role"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  label: Mapped[str] = mapped_column(String(50), nullable=False)

  # Relation
  users: Mapped[List["User"]] = relationship(back_populates="role")


class StudyLevel(Base):
  __tablename__ = "study_level"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  label: Mapped[str] = mapped_column(String(50), nullable=False)

  # Relation
  students: Mapped[List["Student"]] = relationship(back_populates="study_level")


class Job(Base):
  __tablename__ = "Job"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  label: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

  # Relation
  staff_members: Mapped[List["Staff"]] = relationship(back_populates="job_rel")


class AccessLevel(Base):
  __tablename__ = "access_level"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  label: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

  # Relation
  admins: Mapped[List["Admin"]] = relationship(
      back_populates="access_level_rel"
  )


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


class User(Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  lastname: Mapped[str] = mapped_column(String(50), nullable=False)
  firstname: Mapped[str] = mapped_column(String(50), nullable=False)
  email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
  creation_date: Mapped[date] = mapped_column(Date, nullable=False)
  is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
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


class Student(Base):
  __tablename__ = "students"

  id_1: Mapped[int] = mapped_column(
      ForeignKey("users.id"), primary_key=True
  )  # PK et FK vers users
  birth_date: Mapped[date] = mapped_column(Date, nullable=False)
  phone: Mapped[str] = mapped_column(String(50), nullable=False)
  obtained_certification: Mapped[str] = mapped_column(String(50), nullable=False)
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


class Teacher(Base):
  __tablename__ = "teachers"

  id: Mapped[int] = mapped_column(
      ForeignKey("users.id"), primary_key=True
  )  # PK et FK vers users
  specialty: Mapped[str] = mapped_column(String(50), nullable=False)
  hire_date: Mapped[Optional[date]] = mapped_column(Date)
  hourly_rate: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
  biography: Mapped[Optional[str]] = mapped_column(Text)

  # Relations
  user: Mapped["User"] = relationship(back_populates="teacher")
  sessions: Mapped[List["Session"]] = relationship(back_populates="teacher")


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


class Session(Base):
  __tablename__ = "session"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  status: Mapped[str] = mapped_column(
      Enum("OPEN", "CLOSED", "ARCHIVED", name="session_status_enum"),
      nullable=False,
  )
  title: Mapped[Optional[str]] = mapped_column(String(100))
  description: Mapped[Optional[str]] = mapped_column(Text)
  start_date: Mapped[date] = mapped_column(Date, nullable=False)
  end_date: Mapped[date] = mapped_column(Date, nullable=False)
  max_capacity: Mapped[int] = mapped_column(nullable=False)
  prerequisite: Mapped[Optional[str]] = mapped_column(Text)
  id_1: Mapped[str] = mapped_column(
      ForeignKey("classroom.id"), nullable=False
  )  # FK vers classroom
  id_2: Mapped[int] = mapped_column(
      ForeignKey("teachers.id"), nullable=False
  )  # FK vers teachers

  # Relations
  classroom: Mapped["Classroom"] = relationship(back_populates="sessions")
  teacher: Mapped["Teacher"] = relationship(back_populates="sessions")
  registrations: Mapped[List["Registration"]] = relationship(
      back_populates="session"
  )


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