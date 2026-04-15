from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class ChatBase(BaseModel):
    participants: list[UUID]
    name: str | None = None


class ChatCreate(ChatBase):
    pass


class ChatUpdate(BaseModel):
    name: str | None = None


class ChatResponse(ChatBase):
    id: UUID
    is_group: bool
    created_at: datetime
    updated_at: datetime


class ChatReadResponse(BaseModel):
    chat_id: UUID
    read_message_count: int
