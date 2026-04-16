from uuid import UUID, uuid4

from sqlalchemy import Column, Text
from sqlalchemy.dialects import postgresql
from sqlmodel import Field

from .base import Base


class Listing(Base, table=True):
    __tablename__ = "listing"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )

    user_fk: UUID = Field(foreign_key="user.id", nullable=False)
    # seller: User = Relationship(
    #     back_populates="listings",
    #     sa_relationship_kwargs={
    #         "lazy": "selectin",
    #         "foreign_keys": "[User.id]",
    #     },
    # )

    title: str = Field(max_length=64)
    description: str = Field(sa_column=Column(Text))
    manufacturer: str = Field(max_length=128)
    model: str = Field(max_length=64)
    year: int = Field(lt=2100)
    kilometers: float
    price: float
    #
    # comments: list[Comment] = Relationship(
    #     back_populates="listing",
    #     sa_relationship_kwargs={"lazy": "selectin"},
    # )
