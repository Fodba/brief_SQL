from pydantic import BaseModel, ValidationError, Field, field_validator, EmailStr
from datetime import date, datetime

class User(BaseModel):
    """Classe représentant un utilisateur."""

    # Field(min_length=1, max_length=50) --> le nom et prénom doivent au moins comporter un caractère, mais pas
    # plus de 50 caractère
    lastname:str = Field(min_length=1, max_length=50)
    firstname:str = Field(min_length=1, max_length=50)

    email:EmailStr = Field(max_length=255) # EmailStr : vérifie qu'un mail est correct (ex : AUDRIC.GAILLARD97 n'est pas valide")

    # date.today() --> si aucune valeur n'est fournie, prend la date d'aujourd'hui
    creation_date:date=date.today()
    is_active:bool=True # Par défaut : is_active est True
    


    @field_validator("lastname", "firstname")
    @classmethod
    def str_propre(cls, valeur: str)-> str:
        """Renvoie le nom et prénom au propre sans chiffre"""
        if any(caractere.isdigit() for caractere in valeur):
            raise ValueError("Ne doit pas contenir de chiffre")
        return valeur.title()
 
    @field_validator("email")
    @classmethod
    def email_en_minuscules(cls, valeur: str) -> str:
        """Renvoie le mail en minuscule"""
        return valeur.lower()

    @field_validator("creation_date", mode="before")
    @classmethod
    def accepter_date_francaise(cls, valeur):
        """Convertit 'JJ/MM/AAAA' en date. Tout le reste est transmis tel quel à Pydantic."""
        if isinstance(valeur, str) and "/" in valeur:
            return datetime.strptime(valeur.strip(), "%d/%m/%Y").date()
        return valeur


if __name__ == "__main__":
    try:
        new_user=User(lastname="gaillard09", firstname="audric", email="AUDRIC.GAILLARD69@gmail.com", creation_date="31/10/2098")
        print(new_user)
    except ValidationError as e:
        print(e)
  