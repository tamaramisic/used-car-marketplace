from uuid import UUID
from pydantic import BaseModel
from sqlmodel import Field


class BaseComment(BaseModel):
    content: str = Field(min_length=1, max_length=500)


class CommentRead(BaseComment):
    id: UUID
    user_fk: UUID
    listing_fk: UUID


class CommentCreate(BaseComment):
    pass


class CommentUpdate(BaseComment):
    pass
