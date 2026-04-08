from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class BaseComment(BaseModel):
    timestamp: datetime
    content: str

class CommentRead(BaseComment):
    id: UUID

class CommentCreate(BaseComment):
    pass