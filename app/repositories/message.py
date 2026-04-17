from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.repositories.models import Message, MessageReceipts, User
from app.repositories.base_repository import BaseRepository


class MessageRepository(BaseRepository[Message]):
    def __init__(self, db: AsyncSession):
        super().__init__(Message, db)

    async def create_receipts(self, message_id: UUID, user_ids: list[UUID]):
        receipts = [
            MessageReceipts(message_fk=message_id, user_fk=user_id, is_read=False)
            for user_id in user_ids
        ]
        self.db.add_all(receipts)
        await self.db.commit()

    async def get_messages_in_chat(self, chat_id: UUID) -> list[Message]:
        statement = select(Message).where(Message.chat_fk == chat_id)
        result = await self.db.execute(statement)
        return list(result.scalars().all())

    async def get_message(self, message_id: UUID) -> Message | None:
        return await self.find_by(message_id)

    async def get_users_who_read_message(self, message_id: UUID) -> list[User]:
        statement = (
            select(User)
            .join(MessageReceipts)  # SQLAlchemy zna join preko FK
            .where(
                MessageReceipts.message_fk == message_id,
                MessageReceipts.is_read,
            )
        )
        result = await self.db.execute(statement)
        return list(result.scalars().all())
