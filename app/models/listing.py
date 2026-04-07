from sqlalchemy import Column, Text
from sqlmodel import Field
from uuid import UUID, uuid4
from sqlalchemy.dialects import postgresql

from app.models.base import Base


class Listing(Base, table=True):
    __tablename__ = "listing"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )

    user_fk: UUID = Field(foreign_key="user.id", nullable=False) #seller
    title: str = Field(max_length=64)
    description: str = Field(sa_column=Column(Text))
    manufacturer: str = Field(max_length=128)
    model:str = Field(max_length=64)
    year: int = Field(lt = 2100)
    kilometers: float
    price: float
