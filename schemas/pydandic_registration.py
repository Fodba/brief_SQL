from pydantic import BaseModel, ValidationError,field_validator
from datetime import date, datetime
from typing import Literal
# from models import SessionLocal, Session

class Registration(BaseModel):
    """Classe représentant une inscription"""

    register_date:date=date.today()
    presence:bool|None=None

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


    # @model_validator(mode="after")
    # def check_session(self):
    #     with SessionLocal as db:
    #         session=db.query(Session).filter(Session.id==self.id_2).first()
    #         if not session:
    #             raise ValueError("La session n'existe pas")

    #         #


if __name__ == "__main__":
    try:
        print(Registration(register_date='31/10/2003', status="ENREGISTRÉ",id_1=2, id_2=4))
    except ValidationError as e:
        print(e)



