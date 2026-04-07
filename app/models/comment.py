
from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy.dialects import postgresql
from sqlmodel import Column, Field, Relationship
from .base import Base
from .user import User
from .listing import Listing

class Comment(Base, table=True):
    __tablename__="comment"

    id:UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            primary_key=True,
            default=uuid4,
        )
    )

    timestamp:datetime = Field(default=datetime.now(timezone.utc))
    content:str = Field(max_length=250)
    
    author_id:UUID = Field(foreign_key="user.id")
    author:User = Relationship(
        back_populates="comments",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    listing_id:UUID = Field(foreign_key="listing.id")
    listing:Listing = Relationship(
        back_populates="comments",
        sa_relationship_kwargs={"lazy": "selectin"}
    )