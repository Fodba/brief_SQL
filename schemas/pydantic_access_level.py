from pydantic import BaseModel, ValidationError, Field, field_validator
class Role(BaseModel):
    """Classe représentant le niveau d'accès d'un admin."""

    label:str = Field(min_length=1, max_length=50)

    @field_validator("label")
    @classmethod
    def label_propre(cls, valeur: str)-> str:
        """Refuse les chiffre dans le nom du label
        et le renvoie avec une majuscule."""
        if any(caractere.isdigit() for caractere in valeur):
            raise ValueError("Le nom ne doit pas contenir de chiffre")
        return valeur.capitalize()
    
if __name__ == "__main__":
    try:
        print(Role(label="Super Admin"))
    except ValidationError as e:
        print(e)

  