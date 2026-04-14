from app.repositories.message import MessageRepository


class MessageService:
    def __init__(self, repo: MessageRepository):
        self.repo = repo

    # async def send_message(
    #     self,
    #     sender_id: UUID,
    #     receiver_id: UUID,
    #     content: str
    # ) -> Message:
    #
    #     if sender_id == receiver_id:
    #         raise HTTPException(400, "You cannot send a message to yourself")
    #
    #     message = Message(
    #         sender_fk=sender_id,
    #         receiver_fk=receiver_id,
    #         content=content,
    #         created_by=sender_id,
    #     )
    #
    #     return await self.repo.save_or_update(message)
    #
    # async def get_conversation(
    #     self,
    #     user_id: UUID,
    #     other_user_id: UUID
    # ):
    #     return await self.repo.get_conversation(user_id, other_user_id)
    #
    # async def mark_as_read(
    #     self,
    #     message_id: UUID,
    #     user_id: UUID
    # ):
    #     message = await self.repo.get_message_for_user(message_id, user_id)
    #
    #     if not message:
    #         raise HTTPException(404, "Message not found or not allowed")
    #
    #     if message.receiver_fk != user_id:
    #         raise HTTPException(403, "Only receiver can mark as read")
    #
    #     return await self.repo.mark_as_read(message)
    #
    # async def update_message(
    #     self,
    #     message_id: UUID,
    #     user_id: UUID,
    #     content: str | None
    # ):
    #     message = await self.repo.get_message_for_user(message_id, user_id)
    #
    #     if not message:
    #         raise HTTPException(404, "Message not found or not allowed")
    #
    #     if message.sender_fk != user_id:
    #         raise HTTPException(403, "Only sender can edit message")
    #
    #     if content is not None:
    #         message.content = content
    #
    #     message.updated_by = user_id
    #
    #     return await self.repo.save_or_update(message)
    #
    # async def delete_message(
    #     self,
    #     message_id: UUID,
    #     user_id: UUID
    # ):
    #     message = await self.repo.get_message_for_user(message_id, user_id)
    #
    #     if not message:
    #         raise HTTPException(404, "Message not found or not allowed")
    #
    #     # both sender and receiver allowed
    #     await self.repo.delete_by_id(message_id)
    #
    #     return True
    #
    # async def get_message(
    #     self,
    #     message_id: UUID,
    #     user_id: UUID
    # ):
    #     message = await self.repo.get_message_for_user(message_id, user_id)
    #
    #     if not message:
    #         raise HTTPException(404, "Message not found or not allowed")
    #
    #     return message
