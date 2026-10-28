from pydantic import BaseModel, ValidationError, Field, field_validator
from datetime import date, datetime

class Admin(BaseModel):
    """Classe représentant le niveau d'accès d'un admin."""

    id_1:int
    access_level:str = Field(min_length=1, max_length=50)
    promotion_date:date
    id:int

    @field_validator("access_level")
    @classmethod
    def level(cls, valeur: str)-> str:
        """Renvoie le niveau avec une majuscule"""
        if any(caractere.isdigit() for caractere in valeur):
            raise ValueError("Le nom ne doit pas contenir de chiffre")
        return valeur.capitalize()

    @field_validator("promotion_date")
    @classmethod
    def date_francaise(cls, valeur):
        """Convertit 'JJ/MM/AAAA' en date. Tout le reste est transmis tel quel à Pydantic."""
        if isinstance(valeur, str) and "/" in valeur:
            return datetime.strptime(valeur.strip(), "%d/%m/%Y").date()
        return valeur
    
if __name__ == "__main__":
    try:
        Admin(id_1=3, access_level="MAX")
    except ValidationError as e:
        print(e)

  