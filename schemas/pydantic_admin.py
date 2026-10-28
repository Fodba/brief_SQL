from pydantic import BaseModel, ValidationError, Field, field_validator
from datetime import date, datetime

class Admin(BaseModel):
    """Classe représentant un administrateur."""

    id_1:int
    promotion_date:date
    id:int


    @field_validator("promotion_date")
    @classmethod
    def date_francaise(cls, valeur):
        """Convertit 'JJ/MM/AAAA' en date. Tout le reste est transmis tel quel à Pydantic."""
        if isinstance(valeur, str) and "/" in valeur:
            return date.strptime(valeur.strip(), "%Y-%m-%d")
        return valeur
    
if __name__ == "__main__":
    try:
        print(Admin(id_1=3, promotion_date="2026-10-24", id=2))
    except ValidationError as e:
        print(e)

  