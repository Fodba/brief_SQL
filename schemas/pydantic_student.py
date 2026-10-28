from pydantic import BaseModel, ValidationError, Field, field_validator
from datetime import date, datetime
class Student(BaseModel):
    """Classe représentant un étudiant."""

    id_1:int
    birth_date:date
    phone:str = Field(default=None, min_length=1, max_length=50)
