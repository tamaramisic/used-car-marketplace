from uuid import UUID, uuid4
from sqlalchemy.dialects import postgresql
from sqlmodel import Column, Field
from app.models.base import Base

class Message(Base, table=True):
    __tablename__ = "message"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )

    sender_id: UUID = Field(foreign_key="user.id", nullable=False)
    receiver_id: UUID = Field(foreign_key="user.id", nullable=False)
    content: str = Field(nullable=False)
    is_read: bool = Field(default=False)