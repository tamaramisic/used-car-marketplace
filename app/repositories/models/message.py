from uuid import UUID, uuid4
from sqlalchemy.dialects import postgresql
from sqlmodel import Column, Field, Relationship
from .base import Base
from .user import User
from .chat import Chat


class Message(Base, table=True):
    __tablename__ = "message"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )

    sender_fk: UUID = Field(foreign_key="user.id", nullable=False)
    sender: User = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "[Message.sender_fk]",
            "lazy": "selectin",
        },
    )

    chat_fk: UUID = Field(foreign_key="chat.id", nullable=False)
    chat: Chat = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "[Message.chat_fk]",
            "lazy": "selectin",
        },
    )

    content: str = Field(nullable=False)
