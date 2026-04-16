from uuid import UUID
from app.repositories.message import MessageRepository
from app.repositories.models.message import Message


class MessageService:
    def __init__(self, repo: MessageRepository):
        self.repo = repo

    async def create_message_in_chat(
        self, sender_id: UUID, chat_id: UUID, content: str
    ) -> Message:
        message = Message(sender_id=sender_id, chat_id=chat_id, content=content)
        return await self.repo.create_message_in_chat(message)

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
