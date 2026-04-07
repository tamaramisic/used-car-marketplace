from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.models.message import Message


class MessageService:

    @staticmethod
    async def send_message(
        session: AsyncSession,
        sender_id: UUID,
        receiver_id: UUID,
        content: str
    ) -> Message:
        message = Message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
            created_by=sender_id,
        )

        session.add(message)
        await session.commit()
        await session.refresh(message)

        return message

    @staticmethod
    async def get_conversation(
        session: AsyncSession,
        user_id: UUID,
        other_user_id: UUID
    ):
        statement = select(Message).where(
            (
                (Message.sender_id == user_id) &
                (Message.receiver_id == other_user_id)
            )
            |
            (
                (Message.sender_id == other_user_id) &
                (Message.receiver_id == user_id)
            )
        ).order_by(Message.created_at)

        result = await session.exec(statement)
        return result.all()

    @staticmethod
    async def mark_as_read(
        session: AsyncSession,
        message_id: UUID,
        user_id: UUID
    ):
        message = await session.get(Message, message_id)

        if message and message.receiver_id == user_id:
            message.is_read = True
            await session.commit()
            await session.refresh(message)

        return

    @staticmethod
    async def update_message(
            session: AsyncSession,
            message_id: UUID,
            user_id: UUID,
            content: str
    ):
        message = await session.get(Message, message_id)

        if not message:
            return None

        # only sender can edit
        if message.sender_id != user_id:
            return None

        message.content = content
        message.updated_by = user_id

        await session.commit()
        await session.refresh(message)

        return message

    @staticmethod
    async def delete_message(
            session: AsyncSession,
            message_id: UUID,
            user_id: UUID
    ):
        message = await session.get(Message, message_id)

        if not message:
            return False

        # allow sender OR receiver
        if message.sender_id != user_id and message.receiver_id != user_id:
            return False

        await session.delete(message)
        await session.commit()

        return True

    @staticmethod
    async def get_message(
            session: AsyncSession,
            message_id: UUID,
            user_id: UUID
    ):
        message = await session.get(Message, message_id)

        if not message:
            return None

        if message.sender_id != user_id and message.receiver_id != user_id:
            return None

        return message