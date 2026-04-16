# from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    pass


class MessageUpdate(BaseModel):
    content: str | None = None


class MessageResponse(MessageBase):
    message_id: UUID
    # created_at: datetime
    # updated_at: datetime
    # created_by: UUID
    # updated_by: UUID
