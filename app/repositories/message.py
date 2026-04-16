from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.models import Message
from app.repositories.base_repository import BaseRepository


class MessageRepository(BaseRepository[Message]):
    def __init__(self, db: AsyncSession):
        super().__init__(Message, db)

    async def create_message_in_chat(
        self, sender_id: UUID, chat_id: UUID, content: str
    ) -> Message:
        pass

    async def get_messages_in_chat(self):
        pass

    async def get_message_in_chat(self):
        pass

    async def update_message_in_chat(self):
        pass

    async def delete_message_in_chat(self):
        pass

    async def get_users_who_read_message(self):
        pass
