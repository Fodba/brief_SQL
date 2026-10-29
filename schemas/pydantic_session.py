from pydantic import BaseModel, ValidationError, Field, field_validator, model_validator
from datetime import date, datetime
from typing import Literal
from data import SessionLocal
from models import Classroom, Session as SessionModel


class Session(BaseModel):
    """Classe représentant une session"""

    # Literal : autorise seulement les valeurs dans la liste
    status:Literal["OUVERT", "FERMÉ", "ARCHIVÉ"]
    title:str = Field(min_length=1, max_length=100)
    description:str|None=None
    start_date:date
    end_date:date
    max_capacity:int
    prerequisite : str|None=None
    id_1:int
    id_2:int


    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def accepter_date_francaise(cls, valeur):
        """Convertit 'JJ/MM/AAAA' en date. Tout le reste est transmis tel quel à Pydantic."""
        if isinstance(valeur, str) and "/" in valeur:
            return datetime.strptime(valeur.strip(), "%d/%m/%Y").date()
        return valeur

    @model_validator(mode="after")
    def verifier_dates(self):
        if self.start_date>self.end_date:
            raise ValueError("La date de début doit être plus petite que la date de fin")
        return self

    @model_validator(mode="after")
    def verifier_disponibillite(self):
        with SessionLocal() as db:
            classroom = db.query(Classroom).filter(Classroom.id == self.id_1).first()
            if not classroom:
                raise ValueError("La salle n'existe pas")
            if not classroom.is_active:
                raise ValueError("Cette salle n'est pas ouverte.")
            if classroom.capacity < self.max_capacity:
                raise ValueError("Il n'y a pas assez de place dans la salle de classe.")

            classroom_conflit = db.query(SessionModel).filter(
                SessionModel.id_1==self.id_1,
                SessionModel.start_date<=self.end_date,
                SessionModel.end_date>=self.start_date              
            ).first()

            if classroom_conflit:
                raise ValueError("La salle est déjà réservé entre ces dates")

            teacher_conflit = db.query(SessionModel).filter(
                SessionModel.id_2==self.id_2,
                SessionModel.start_date<=self.end_date,
                SessionModel.end_date>=self.start_date              
            ).first()

            if teacher_conflit:
                raise ValueError("L'enseignant est déjà assigné à une autre session entre ces dates")
        return self

if __name__ == "__main__":
    try:
        print(Session(status="OUVERT", title="Test", start_date="26/10/2026", end_date="27/10/2026", max_capacity=12, id_1=3, id_2=1))
    except ValidationError as e:
        print(e)

