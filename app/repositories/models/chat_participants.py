from uuid import UUID, uuid4

from sqlalchemy.dialects import postgresql
from sqlmodel import Column, Field, Relationship

from .base import Base
from .user import User
from .chat import Chat


class ChatParticipants(Base, table=True):
    __tablename__ = "chat_participants"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )

    participant_fk: UUID = Field(foreign_key="user.id", nullable=False)
    participant: User = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "[ChatParticipants.participant_fk]",
            "lazy": "selectin",
        },
    )

    chat_fk: UUID = Field(foreign_key="chat.id", nullable=False)
    chat: Chat = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "[ChatParticipants.chat_fk]",
            "lazy": "selectin",
        },
    )
