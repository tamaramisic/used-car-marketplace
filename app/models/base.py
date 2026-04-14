from datetime import datetime, timezone
from uuid import UUID
from sqlmodel import Field, SQLModel


class Base(SQLModel):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    created_by: UUID | None = Field(default=None, foreign_key="user.id")
    updated_by: UUID | None = Field(default=None, foreign_key="user.id")
