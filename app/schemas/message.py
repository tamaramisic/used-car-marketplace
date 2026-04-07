from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    receiver_id: UUID

class MessageUpdate(BaseModel):
    content: str | None

class MessageResponse(MessageBase):
    id: UUID
    sender_id: UUID
    receiver_id: UUID
    is_read: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes":True}