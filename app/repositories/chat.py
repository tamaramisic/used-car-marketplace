from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.models import Chat
from app.repositories.base_repository import BaseRepository


class ChatRepository(BaseRepository[Chat]):
    def __init__(self, db: AsyncSession):
        super().__init__(Chat, db)

    async def create_chat(self, participant_ids: list[UUID]) -> Chat:
        pass

    async def add_participants(
        self, chat_id: UUID, participant_ids: list[UUID]
    ) -> Chat:
        pass

    async def get_chats(self):
        pass

    async def get_chat(self):
        pass

    async def update_chat(self):
        pass

    async def delete_chat(self):
        pass

    async def mark_chat_read(self):
        pass
