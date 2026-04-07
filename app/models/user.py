from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlalchemy.dialects import postgresql
from sqlmodel import Column, Field, Relationship

from .base import Base

class User(Base, table=True):
    __tablename__ = "user"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )

    username: str = Field(max_length=64)
    email: EmailStr = Field(unique=True, index=True)
    full_name: str = Field(max_length=64)
    phone: str | None = None

    comments: list["Comment"] = Relationship(
        back_populates="author",
        sa_relationship_kwargs={
            "lazy": "selectin",
        },
    )

    listings: list["Listing"] = Relationship(
        back_populates="seller",
        sa_relationship_kwargs={
            "lazy": "selectin",
        },
    )

    sent_messages: list["Message"] = Relationship(
        back_populates="sender",
        sa_relationship_kwargs={
            "foreign_keys": "[Message.sender_fk]",
            "lazy": "selectin",
        },
    )

    received_messages: list["Message"] = Relationship(
        back_populates="receiver",
        sa_relationship_kwargs={
            "foreign_keys": "[Message.receiver_fk]",
            "lazy": "selectin",
        },
    )
