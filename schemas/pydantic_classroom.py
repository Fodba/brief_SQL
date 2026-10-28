from pydantic import BaseModel, ValidationError, Field, field_validator
class Classroom(BaseModel):
    """Classe représentant le niveau d'accès d'un admin."""

    name:str = Field(min_length=1, max_length=50) # au moins 1 caractère, mais pas plus de 50 caractères
    capacity:int
    location:str = Field(min_length=1, max_length=50) # au moins 1 caractère, mais pas plus de 50 caractères
    is_active:bool=True # True par défaut
    equipment:str

    @field_validator("name")
    @classmethod
    def str_propre(cls, valeur: str)-> str:
        """Renvoie le nom de la classe au propre """
        return valeur.capitalize()
    
if __name__ == "__main__":
    try:
        print(Classroom(name="Salle informatique", capacity=17, location="Salle 201", equipment="PC, projecteur, souris"))
    except ValidationError as e:
        print(e)

  