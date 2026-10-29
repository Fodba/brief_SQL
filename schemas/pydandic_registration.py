from pydantic import BaseModel, ValidationError,field_validator, model_validator, ConfigDict
from datetime import date, datetime
from typing import Literal
from models import Session as SessionModel, Registration as RegistrationModel
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
            if session.status!="OUVERT":
                raise ValueError("La session n'est pas ouverte.")
            count=db.query(RegistrationModel).filter(RegistrationModel.id_2==self.id_2).count()
            if count>=session.max_capacity:
                raise ValueError("Plus de place dans la session.")
            conflit = (
                db.query(RegistrationModel).join(SessionModel, RegistrationModel.id_2 == SessionModel.id) # Jointure pour accéder aux dates de la session
                .filter(
                    RegistrationModel.id_1 == self.id_1,
                    SessionModel.start_date<=session.end_date,
                    SessionModel.end_date>=session.start_date  
                    )                     # Pour cet étudiant spécifique                                   # Dont les dates se croisent)
                .first()
            )
            if conflit:
                raise ValueError("Cette étudiant est inscrit à une autre session entre ces deux dates")
        return self

    
if __name__ == "__main__":
    try:
        print(Registration(register_date='31/10/2003', status="ENREGISTRÉ",id_1=2, id_2=1))
    except ValidationError as e:
        print(e)



