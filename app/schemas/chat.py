# from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class ChatBase(BaseModel):
    name: str | None = None
    is_group: bool = False


class ChatCreate(ChatBase):
    participant_ids: list[UUID]


class ChatUpdate(BaseModel):
    name: str | None = None


class ChatResponse(ChatBase):
    chat_id: UUID
    # created_at: datetime
    # updated_at: datetime
    # created_by: UUID
    # updated_by: UUID


class ChatUpdateRead(BaseModel):
    is_chat_read: bool


class ChatReadResponse(ChatResponse):
    is_chat_read: bool
