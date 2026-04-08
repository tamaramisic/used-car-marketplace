from uuid import UUID
from typing import List

from sqlmodel import select

from app.models.message import Message
from app.repositories.base_repository import BaseRepository
from app.dependencies import SessionDep


class MessageRepository(BaseRepository[Message]):

    def __init__(self, db: SessionDep):
        super().__init__(Message, db)

    async def get_conversation(
        self,
        user_id: UUID,
        other_user_id: UUID
    ) -> List[Message]:

        statement = select(Message).where(
            (
                (Message.sender_fk == user_id) &
                (Message.receiver_fk == other_user_id)
            )
            |
            (
                (Message.sender_fk == other_user_id) &
                (Message.receiver_fk == user_id)
            )
        ).order_by(Message.created_at)

        result = await self.db.exec(statement)
        return result.all()

    async def get_message_for_user(
        self,
        message_id: UUID,
        user_id: UUID
    ) -> Message | None:

        message = await self.db.get(Message, message_id)

        if not message:
            return None

        if message.sender_fk != user_id and message.receiver_fk != user_id:
            return None

        return message

    async def mark_as_read(
        self,
        message: Message
    ) -> Message:

        message.is_read = True
        self.db.add(message)

        await self.db.commit()
        await self.db.refresh(message)

        return message