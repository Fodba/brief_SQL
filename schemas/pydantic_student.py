from pydantic import BaseModel, ValidationError, Field, field_validator, model_validator, ConfigDict
from datetime import date, datetime
class Student(BaseModel):
    """Classe représentant un étudiant."""

    id_1:int
    birth_date:date
    phone:str = Field(default=None, min_length=1, max_length=50)
    obtained_certification:str = Field(default=None, min_length=1, max_length=50)
    registration_date:date=date.today()
    id:int

    model_config = ConfigDict(from_attributes=True)

    @field_validator("birth_date", "registration_date", mode="before")
    @classmethod
    def accepter_date_francaise(cls, valeur):
        """Convertit 'JJ/MM/AAAA' en date. Tout le reste est transmis tel quel à Pydantic."""
        if isinstance(valeur, str) and "/" in valeur:
            return datetime.strptime(valeur.strip(), "%d/%m/%Y").date()
        return valeur

    @field_validator("phone")
    @classmethod
    def telephone_normalise(cls, valeur: str | None) -> str | None:
        """Ramène un numéro français au format '06 12 34 56 78'."""
        if valeur is None:
            return None
        chiffres = "".join(caractere for caractere in valeur if caractere.isdigit())
        if len(chiffres) == 11 and chiffres.startswith("33"):   # +33 6 12... devient 06 12...
            chiffres = "0" + chiffres[2:]
        if len(chiffres) != 10 or not chiffres.startswith("0"):
            raise ValueError("numéro de téléphone français attendu (10 chiffres)")
        return " ".join(chiffres[i:i + 2] for i in range(0, 10, 2))


    @model_validator(mode="after")
    def verifier_age(self):
        """Vérifie si l'étudiant a plus de 16 ans"""
        if date.today().year - self.birth_date.year < 16:
            raise ValueError("L'étudiant doit avoir plus de 16 ans")
        return self
    
        
if __name__ == "__main__":
    try:
        print(Student(id_1 = 4, birth_date="31/10/2000", phone="+33102030405", obtained_certification="Bachelor, orientation 'Technologie'", id=3))
    except ValidationError as e:
        print(e)
