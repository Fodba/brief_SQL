from pydantic import BaseModel, ValidationError, field_validator, Field, model_validator, ConfigDict
from datetime import date, datetime
from decimal import Decimal

class Teacher(BaseModel):
    """Classe représentant un enseignant"""
    id:int
    specialty:str=Field(min_length=1, max_length=50)
    hire_date:date
    hourly_rate:Decimal
    biography:str|None=None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("hire_date", mode="before")
    @classmethod
    def accepter_date_francaise(cls, valeur):
        """Convertit 'JJ/MM/AAAA' en date. Tout le reste est transmis tel quel à Pydantic."""
        if isinstance(valeur, str) and "/" in valeur:
            return datetime.strptime(valeur.strip(), "%d/%m/%Y").date()
        return valeur

    @model_validator(mode="after")
    def verifier_date_embauche(self):
        """Vérifie la date d'embauche"""
        if self.hire_date > date.today():
            raise ValueError("La date d'embauche dépasse la date d'aujourd'hui.")

if __name__ == "__main__":
    try:
        print(Teacher(id = 4, specialty="Python", hire_date="27/10/2026", hourly_rate=34.8))
    except ValidationError as e:
        print(e)