from pydantic import BaseModel, ValidationError, field_validator
from datetime import date, datetime

class Staff(BaseModel):
    """Classe représentant un membre du staff"""
    id_1:int
    start_date:date
    responsabilities:str
    id:int

    @field_validator("start_date", mode="before")
    @classmethod
    def accepter_date_francaise(cls, valeur):
        """Convertit 'JJ/MM/AAAA' en date. Tout le reste est transmis tel quel à Pydantic."""
        if isinstance(valeur, str) and "/" in valeur:
            return datetime.strptime(valeur.strip(), "%d/%m/%Y").date()
        return valeur


if __name__ == "__main__":
    try:
        print(Staff(id_1 = 4, start_date="27/10/2026", responsabilities="Nettoyer les toilettes", id=3))
    except ValidationError as e:
        print(e)