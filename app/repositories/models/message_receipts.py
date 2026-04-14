from uuid import UUID, uuid4

from sqlalchemy.dialects import postgresql
from sqlmodel import Column, Field, Relationship

from .base import Base
from .user import User
from .message import Message


class MessageReceipts(Base, table=True):
    __tablename__ = "message_receipts"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )

    user_fk: UUID = Field(foreign_key="user.id", nullable=False)
    user: User = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "[MessageReceipts.user_fk]",
            "lazy": "selectin",
        },
    )

    message_fk: UUID = Field(foreign_key="message.id", nullable=False)
    message: Message = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "[MessageReceipts.message_fk]",
            "lazy": "selectin",
        },
    )

    is_read: bool = Field(default=False)
