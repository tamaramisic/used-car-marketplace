from pydantic import BaseModel, Field


class ListingSave(BaseModel):
    title: str = Field(max_length=64)
    description: str
    manufacturer: str = Field(max_length=128)
    model: str = Field(max_length=64)
    year: int = Field(lt=2100)
    kilometers: float
    price: float
