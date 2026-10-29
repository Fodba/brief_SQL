from pydantic import BaseModel, ValidationError, field_validator, ConfigDict
from datetime import date, datetime

class Admin(BaseModel):
    """Classe représentant un administrateur."""

    id_1:int
    promotion_date:date
    id:int

    model_config = ConfigDict(from_attributes=True)

    @field_validator("promotion_date", mode="before")
    @classmethod
    def accepter_date_francaise(cls, valeur):
        """Convertit 'JJ/MM/AAAA' en date. Tout le reste est transmis tel quel à Pydantic."""
        if isinstance(valeur, str) and "/" in valeur:
            return datetime.strptime(valeur.strip(), "%d/%m/%Y").date()
        return valeur
    
if __name__ == "__main__":
    try:
        print(Admin(id_1=3, promotion_date="24/10/2026", id=2))
    except ValidationError as e:
        print(e)

  