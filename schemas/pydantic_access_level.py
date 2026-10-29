from pydantic import BaseModel, ValidationError, Field, field_validator, ConfigDict
class AccessLevel(BaseModel):
    """Classe représentant le niveau d'accès d'un admin."""

    # Field(min_length=1, max_length=50) --> au moins un caractère dans le champ, mais pas plus de 50 caractère
    label:str = Field(min_length=1, max_length=50)

    model_config = ConfigDict(from_attributes=True)

    @field_validator("label")
    @classmethod
    def label_propre(cls, valeur: str)-> str:
        """Refuse les chiffre dans le nom du niveau d'accès et le renvoie en majuscule."""
        if any(caractere.isdigit() for caractere in valeur):
            raise ValueError("Le nom ne doit pas contenir de chiffre")
        return valeur.upper()
    
if __name__ == "__main__":
    try:
        print(AccessLevel(label="SuperAdmin"))
    except ValidationError as e:
        print(e)

  