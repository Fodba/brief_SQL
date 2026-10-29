from pydantic import BaseModel, ValidationError,field_validator, model_validator, ConfigDict
from datetime import date, datetime
from typing import Literal

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
    
if __name__ == "__main__":
    try:
        print(Registration(register_date='31/10/2003', status="ENREGISTRÉ",id_1=2, id_2=1))
    except ValidationError as e:
        print(e)



