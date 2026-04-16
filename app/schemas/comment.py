from uuid import UUID
from pydantic import BaseModel


class BaseComment(BaseModel):
    content: str


class CommentRead(BaseComment):
    id: UUID
    author_id: UUID
    listing_fk: UUID


class CommentCreate(BaseComment):
    id: UUID
    listing_fk: UUID
