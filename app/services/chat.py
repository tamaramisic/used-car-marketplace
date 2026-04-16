# from uuid import UUID
from app.repositories.chat import ChatRepository
# from app.repositories.models.chat import Chat


class ChatService:
    def __init__(self, repo: ChatRepository):
        self.repo = repo

    async def create_chat(self):
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
