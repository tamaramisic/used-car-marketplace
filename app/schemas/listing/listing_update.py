from pydantic import BaseModel, Field


class ListingUpdate(BaseModel):
    title: str  | None = Field(None, max_length=64)
    description: str | None = None
    kilometers: float | None = None
    price: float | None = None