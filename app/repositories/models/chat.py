from uuid import UUID, uuid4
from sqlalchemy.dialects import postgresql
from sqlmodel import Column, Field
from .base import Base


class Chat(Base, table=True):
    __tablename__ = "chat"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )

    name: str = Field(nullable=False)
    is_group: bool = Field(default=False)
