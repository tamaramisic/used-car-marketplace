from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.repositories.models import Chat, ChatParticipants
from app.repositories.base_repository import BaseRepository


class ChatRepository(BaseRepository[Chat]):
    def __init__(self, db: AsyncSession):
        super().__init__(Chat, db)

    async def add_participants(self, chat_id: UUID, participant_ids: list[UUID]):
        participants = [
            ChatParticipants(participant_fk=user_id, chat_fk=chat_id)
            for user_id in participant_ids
        ]
        self.db.add_all(participants)
        await self.db.commit()

    async def get_chats(self, user_id: UUID) -> list[Chat]:
        statement = (
            select(Chat)
            .join(ChatParticipants)  # SQLAlchemy zna join preko FK
            .where(ChatParticipants.participant_fk == user_id)
        )
        result = await self.db.execute(statement)
        return list(result.scalars().all())

    async def get_chat_participants(self, chat_id: UUID) -> list[UUID]:
        statement = select(ChatParticipants.participant_fk).where(
            ChatParticipants.chat_fk == chat_id
        )
        result = await self.db.execute(statement)
        return list(result.scalars().all())

    async def is_user_in_chat(self, chat_id: UUID, user_id: UUID) -> bool:
        statement = select(ChatParticipants).where(
            ChatParticipants.chat_fk == chat_id,
            ChatParticipants.participant_fk == user_id,
        )
        result = await self.db.execute(statement)
        return result.scalar_one_or_none() is not None
