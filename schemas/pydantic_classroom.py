from pydantic import BaseModel, ValidationError, Field, field_validator
class Classroom(BaseModel):
    """Classe représentant une salle de classe"""

    name:str = Field(min_length=1, max_length=50) # au moins 1 caractère, mais pas plus de 50 caractères
    capacity:int = Field(ge=1) # doit être égal ou valoir plus que 1
    location:str = Field(min_length=1, max_length=50) # au moins 1 caractère, mais pas plus de 50 caractères
    is_active:bool=True # True par défaut
    equipments:str


    @field_validator("name", "location")
    @classmethod
    def str_propre(cls, valeur: str)-> str:
        """Renvoie le nom de la classe et sa localisation au propre"""
        return valeur.capitalize()
    
if __name__ == "__main__":
    try:
        print(Classroom(name="Salle informatique", capacity=1, location="salle 201", equipments="PC, projecteur, souris"))
    except ValidationError as e:
        print(e)

  