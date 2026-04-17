from uuid import UUID
from fastapi import HTTPException
from app.repositories.chat import ChatRepository
from app.repositories.models import Chat
from app.repositories.user import UserRepository


class ChatService:
    def __init__(self, repo: ChatRepository, user_repo: UserRepository):
        self.repo = repo
        self.user_repo = user_repo

    async def create_chat(self, name: str, keycloak_id, participant_ids):
        user = await self.user_repo.find_by_keycloak_id(keycloak_id)
        all_participants = list(set([user.id] + participant_ids))
        print("keycloak_id:", keycloak_id)
        print("participant_ids:", participant_ids)
        print("current_user:", user.id)

        chat = Chat(name=name, is_group=len(all_participants) > 2)
        chat = await self.repo.create(chat)
        await self.repo.add_participants(chat.id, all_participants)
        return chat

    async def get_chats(self, user_id: UUID):
        await self.repo.get_chats(user_id)

    async def get_chat(self, chat_id: UUID, user_id: UUID):
        if not await self.repo.is_user_in_chat(chat_id, user_id):
            raise HTTPException(status_code=403, detail="Not allowed")

        chat = await self.repo.find_by(chat_id)
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        return chat

    async def update_chat(self, chat_id: UUID, user_id: UUID, name: str):
        chat = await self.get_chat(chat_id, user_id)
        if name:
            chat.name = name
        return await self.repo.update(chat)

    async def delete_chat(self, chat_id: UUID, user_id: UUID):
        chat = await self.get_chat(chat_id, user_id)
        await self.repo.delete(chat)
        return chat

    async def mark_chat_read(self, chat_id: UUID, is_chat_read: bool, user_id: UUID):
        if not await self.repo.is_user_in_chat(chat_id, user_id):
            raise HTTPException(status_code=403, detail="Not allowed")
        return {
            "chat_id": chat_id,
            "is_chat_read": is_chat_read,
        }
