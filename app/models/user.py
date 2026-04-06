from datetime import datetime, timezone
from uuid import UUID, uuid4
from pydantic import EmailStr
from sqlalchemy.dialects import postgresql
from sqlmodel import Column, Field, SQLModel

class Base(SQLModel):
    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now(timezone.utc),
        )
    )

    updated_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now(timezone.utc),
        )
    )

    created_by: UUID | None = Field(default=None, foreign_key="user.id")

    updated_by: UUID | None = Field(default=None, foreign_key="user.id")

class User(Base, table=True):
    __tablename__="user"

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