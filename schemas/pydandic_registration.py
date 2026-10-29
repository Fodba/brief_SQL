from pydantic import BaseModel, ValidationError,field_validator, model_validator, ConfigDict
from datetime import date, datetime
from typing import Literal
from models import Session as SessionModel, Registration, Student
from data import SessionLocal

class Registration(BaseModel):
    """Classe représentant une inscription"""

    register_date:date=date.today()
    presence:bool|None=None # Par défaut, None

    # Literal : autorise seulement les valeurs dans la liste
    status:Literal["ENREGISTRÉ", "DÉSINSCRIT", "EN_ATTENTE"]
    id_1:int
    id_2:int

    model_config=ConfigDict(from_attributes=True)

    @field_validator("register_date", mode="before")
    @classmethod
    def accepter_date_francaise(cls, valeur):
        """Convertit 'JJ/MM/AAAA' en date. Tout le reste est transmis tel quel à Pydantic."""
        if isinstance(valeur, str) and "/" in valeur:
            return datetime.strptime(valeur.strip(), "%d/%m/%Y").date()
        return valeur

    @model_validator(mode="after")
    def check_session_status(self):
        with SessionLocal() as db:

            session = db.query(SessionModel).filter(SessionModel.id == self.id_2).first()
            if not session:
                raise ValueError("La session n'existe pas.")
            if session.status!="OPEN":
                raise ValueError("La session n'est pas ouverte.")
            count=db.query(Registration).count()
            if count>=session.max_capacite:
                raise ValueError("Plus de place dans la session.")
        return self

    @model_validator(mode="after")
    def check_date_overlap(self):
        with SessionLocal() as db:
            session = db.query(SessionModel).join(SessionModel.id == self.id_2).first()
            if not session:
                raise ValueError("Session non-existante")
            if session.end_date < self.register_date:
                raise ValueError("Impossible de s'inscrire après la date de fin de la session")

            overlap = db.query(Registration).join(SessionModel, Registration.id_2 == SessionModel.id).filter(
                Registration.id_1==self.id_1,
                Registration.id_2!=self.id_2,
                SessionModel.start_date <= session.end_date,
                SessionModel.end_date >= session.start_date,
            )
            if overlap:
                raise ValueError("Chevauchement de date")

        return self
if __name__ == "__main__":
    try:
        print(Registration(register_date='31/10/2003', status="ENREGISTRÉ",id_1=2, id_2=1))
    except ValidationError as e:
        print(e)



