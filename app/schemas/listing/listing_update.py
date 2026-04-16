from pydantic import BaseModel


class ListingUpdate(BaseModel):
    description: str | None = None
    kilometers: float | None = None
    price: float | None = None
