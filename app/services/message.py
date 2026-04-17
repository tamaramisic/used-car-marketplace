from uuid import UUID
from fastapi import HTTPException
from app.repositories.chat import ChatRepository
from app.repositories.message import MessageRepository
from app.repositories.models.message import Message


class MessageService:
    def __init__(self, repo: MessageRepository, chat_repo: ChatRepository):
        self.repo = repo
        self.chat_repo = chat_repo

    async def create_message_in_chat(
        self, chat_id: UUID, sender_id: UUID, content: str
    ):
        if not await self.chat_repo.is_user_in_chat(chat_id, sender_id):
            raise HTTPException(status_code=403, detail="Not allowed")
        message = Message(
            chat_id=chat_id,
            sender_id=sender_id,
            content=content,
        )
        message = await self.repo.create(message)

        participants = await self.chat_repo.get_chat_participants(chat_id)
        await self.repo.create_receipts(message.id, participants)

        return message

    async def get_messages_in_chat(self, chat_id: UUID, sender_id: UUID):
        if not await self.chat_repo.is_user_in_chat(chat_id, sender_id):
            raise HTTPException(status_code=403)
        return await self.repo.get_messages_in_chat(chat_id)

    async def get_message_in_chat(
        self, chat_id: UUID, message_id: UUID, sender_id: UUID
    ):
        message = await self.repo.get_message(message_id)
        if not message or message.chat_fk != chat_id:
            raise HTTPException(status_code=404)
        if not await self.chat_repo.is_user_in_chat(chat_id, sender_id):
            raise HTTPException(status_code=403)
        return message

    async def update_message_in_chat(
        self, chat_id: UUID, message_id: UUID, sender_id: UUID, content: str | None
    ):
        message = await self.get_message_in_chat(chat_id, message_id, sender_id)
        if message.sender_fk != sender_id:
            raise HTTPException(status_code=403)
        if content:
            message.content = content
        return await self.repo.update(message)

    async def delete_message_in_chat(
        self, chat_id: UUID, message_id: UUID, sender_id: UUID
    ):
        message = await self.get_message_in_chat(chat_id, message_id, sender_id)
        await self.repo.delete(message)
        return message

    async def get_users_who_read_message(
        self, chat_id: UUID, message_id: UUID, user_id: UUID
    ):
        if not await self.chat_repo.is_user_in_chat(chat_id, user_id):
            raise HTTPException(status_code=403)
        return await self.repo.get_users_who_read_message(message_id)
