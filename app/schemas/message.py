from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    pass
    # chat_id: UUID


class MessageUpdate(BaseModel):
    content: str | None = None


class MessageResponse(MessageBase):
    id: UUID
    # sender_id: UUID
    # chat_id: UUID
    is_read: bool
    created_at: datetime
    updated_at: datetime


class MessageReadResponse(BaseModel):
    message_id: UUID
    is_read: bool
