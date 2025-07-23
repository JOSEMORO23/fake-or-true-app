from pydantic import BaseModel, Field, validator

class NewsInput(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    text: str = Field(..., min_length=20)

    @validator("title", "text")
    def must_have_letters(cls, value: str) -> str:
        # Verifica si al menos el 30% del contenido son letras
        letter_count = sum(c.isalpha() for c in value)
        if letter_count < len(value) * 0.3:
            raise ValueError("El texto debe contener más contenido alfabético.")
        return value
    