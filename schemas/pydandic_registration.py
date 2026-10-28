from pydantic import BaseModel, ValidationError,field_validator, model_validator, ValidationInfo
from datetime import date, datetime
from typing import Literal
from models import *

class Registration(BaseModel):
    """Classe représentant une inscription"""

    register_date:date=date.today()
    presence:bool|None=None # Par défaut, None

    # Literal : autorise seulement les valeurs dans la liste
    status:Literal["ENREGISTRÉ", "DÉSINSCRIT", "EN_ATTENTE"]
    id_1:int
    id_2:int

    @field_validator("register_date", mode="before")
    @classmethod
    def accepter_date_francaise(cls, valeur):
        """Convertit 'JJ/MM/AAAA' en date. Tout le reste est transmis tel quel à Pydantic."""
        if isinstance(valeur, str) and "/" in valeur:
            return datetime.strptime(valeur.strip(), "%d/%m/%Y").date()
        return valeur


    @model_validator(mode="after")
    def check_session(self, info:ValidationInfo)->"Registration":
        context = info.context
        if context and "db_session" in context:
            db = context["db_session"]
        session_db =db.get(Session, self.id_2)
        if not session_db:
            raise ValueError("La session n'existe pas")
        


if __name__ == "__main__":
    try:
        print(Session(status="OUVERT", title="Test", start_date="26/10/2026", end_date="27/10/2026", max_capacity=12, id_1=3, id_2=1))
        print(Registration(register_date='31/10/2003', status="ENREGISTRÉ",id_1=2, id_2=1))
    except ValidationError as e:
        print(e)



