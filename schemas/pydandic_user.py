from pydantic import BaseModel, ValidationError, Field, field_validator, EmailStr
from datetime import date, datetime

class User(BaseModel):
    """Classe représentant un niveau utilisateur."""

    # Field(min_length=1, max_length=50) --> le nom et prénom doivent au moins comporter un caractère, mais pas
    # plus de 50 caractère
    lastname:str = Field(min_length=1, max_length=50)
    firstname:str = Field(min_length=1, max_length=50)

    email:EmailStr = Field(max_length=255) # EmailStr : vérifie qu'un mail est correct (ex : AUDRIC.GAILLARD97 n'est pas valide")

    # datetime.now().strftime("%Y/%m/%d") --> si aucune valeur n'est fournie, prend la date d'aujourd'hui et le
    # restitue sous le format : 2026-10-28
    creation_date:date=datetime.now().strftime("%Y")
    is_active:bool=True # Par défaut : is_active est True
    


    @field_validator("lastname", "firstname")
    @classmethod
    def str_propre(cls, valeur: str)-> str:
        """Renvoie le nom et prénom au propre sans chiffre"""
        if any(caractere.isdigit() for caractere in valeur):
            raise ValueError("Ne doit pas contenir de chiffre")
        return valeur.capitalize()

    @field_validator("email")
    @classmethod
    def email_en_minuscules(cls, valeur: str) -> str:
        """Renvoie le mail en minuscule"""
        return valeur.lower()


if __name__ == "__main__":
    try:
        new_user=User(lastname="gaillard", firstname="audric", email="AUDRIC.GAILLARD97@gmail.com")
        print(new_user)
    except ValidationError as e:
        print(e)
  