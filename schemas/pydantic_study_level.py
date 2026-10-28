from pydantic import BaseModel, ValidationError, Field, field_validator
class StudyLevel(BaseModel):
    """Classe représentant le niveau d'études d'un étudiant."""

    label:str = Field(min_length=1, max_length=50)

    @field_validator("label")
    @classmethod
    def label_propre(cls, valeur: str)-> str:
        """Renvoie le niveau d'études au propre"""
        return valeur.capitalize()

if __name__ == "__main__":
    try:
        study = StudyLevel(label="bac +3")
        print(study.label)
    except ValidationError as e:
        print(e)

  