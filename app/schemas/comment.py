from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class BaseComment(BaseModel):
    content: str

class CommentRead(BaseComment):
    comment_id: UUID
    author_id: UUID

class CommentCreate(BaseComment):
    pass