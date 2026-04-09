from pydantic import BaseModel, Field


class ListingUpdate(BaseModel):
    title: str = Field(max_length=64)
    description: str
    kilometers: float
    price: float