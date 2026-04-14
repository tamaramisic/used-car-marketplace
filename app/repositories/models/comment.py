from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy.dialects import postgresql
from sqlmodel import Column, Field, Relationship

from .base import Base
from .user import User


class Comment(Base, table=True):
    __tablename__ = "comment"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            primary_key=True,
            default=uuid4,
        )
    )

    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    content: str = Field(max_length=250)

    user_fk: UUID = Field(foreign_key="user.id")
    author: User = Relationship(
        back_populates="comments",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "foreign_keys": "[Comment.user_fk]",
        },
    )

    listing_fk: UUID = Field(foreign_key="listing.id")
