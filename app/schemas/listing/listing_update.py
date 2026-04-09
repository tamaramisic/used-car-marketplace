from uuid import UUID

from pydantic import BaseModel, Field


class ListingUpdate(BaseModel):
    id: UUID
    title: str = Field(max_length=64)
    description: str
    kilometers: float
    price: float