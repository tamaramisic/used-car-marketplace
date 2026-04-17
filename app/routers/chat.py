from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Depends

from app.core.dependencies import (
    ChatRepositoryDep,
    MessageRepositoryDep,
    CurrentUserDep,
    UserRepositoryDep,
)
from app.schemas.user_read import UserRead
from app.schemas.message import (
    MessageResponse,
    MessageCreate,
    MessageUpdate,
)
from app.schemas.chat import (
    ChatResponse,
    ChatCreate,
    ChatUpdate,
    ChatUpdateRead,
    ChatReadResponse,
)

from app.services.message import MessageService
from app.services.chat import ChatService

router = APIRouter(prefix="/chats", tags=["Chat"])


######### chat service dependency
async def get_chat_service(
    repo: ChatRepositoryDep, user_repo: UserRepositoryDep
) -> ChatService:
    return ChatService(repo, user_repo)


ChatServiceDep = Annotated[ChatService, Depends(get_chat_service)]


######### message service dependency
async def get_message_service(
    repo: MessageRepositoryDep, chat_repo: ChatRepositoryDep
) -> MessageService:
    return MessageService(repo, chat_repo)


MessageServiceDep = Annotated[MessageService, Depends(get_message_service)]


######### CHAT
@router.post("/", response_model=ChatResponse)
async def create_chat(
    body: ChatCreate,
    service: ChatServiceDep,
    current_user: CurrentUserDep,
):
    return await service.create_chat(
        name=body.name,
        keycloak_id=current_user.keycloak_id,
        participant_ids=body.participant_ids,
    )


@router.get("/", response_model=list[ChatResponse])
async def get_chats(
    service: ChatServiceDep,
    current_user: CurrentUserDep,
):
    return await service.get_chats(
        keycloak_id=current_user.keycloak_id,
    )


@router.get("/{chat_id}", response_model=ChatResponse)
async def get_chat(
    chat_id: UUID,
    service: ChatServiceDep,
    current_user: CurrentUserDep,
):
    return await service.get_chat(
        chat_id=chat_id,
        keycloak_id=current_user.keycloak_id,
    )


@router.put("/{chat_id}", response_model=ChatResponse)
async def update_chat(
    chat_id: UUID,
    body: ChatUpdate,
    service: ChatServiceDep,
    current_user: CurrentUserDep,
):
    return await service.update_chat(
        chat_id=chat_id,
        keycloak_id=current_user.keycloak_id,
        name=body.name,
    )


@router.delete("/{chat_id}", response_model=ChatResponse)  # ONLY ADMIN
async def delete_chat(
    chat_id: UUID,
    service: ChatServiceDep,
    current_user: CurrentUserDep,
):
    return await service.delete_chat(
        chat_id=chat_id,
        keycloak_id=current_user.keycloak_id,
    )


@router.post("/{chat_id}/read", response_model=ChatReadResponse)
async def mark_chat_as_read(  # current user opens chat == current user read all messages in chat
    chat_id: UUID,
    body: ChatUpdateRead,
    service: ChatServiceDep,
    current_user: CurrentUserDep,
):
    return await service.mark_chat_read(
        chat_id=chat_id,
        is_chat_read=body.is_chat_read,
        keycloak_id=current_user.keycloak_id,
    )


######### MESSAGE
@router.post("/{chat_id}/messages", response_model=MessageResponse)
async def create_message_in_chat(
    chat_id: UUID,
    body: MessageCreate,
    service: MessageServiceDep,
    current_user: CurrentUserDep,
):
    return await service.create_message_in_chat(
        chat_id=chat_id,
        keycloak_id=current_user.keycloak_id,
        content=body.content,
    )


@router.get("/{chat_id}/messages", response_model=list[MessageResponse])
async def get_messages_in_chat(
    chat_id: UUID, service: MessageServiceDep, current_user: CurrentUserDep
):
    return await service.get_messages_in_chat(
        chat_id=chat_id,
        keycloak_id=current_user.keycloak_id,
    )


@router.get("/{chat_id}/messages/{message_id}", response_model=MessageResponse)
async def get_message_in_chat(
    chat_id: UUID,
    message_id: UUID,
    service: MessageServiceDep,
    current_user: CurrentUserDep,
):
    return await service.get_message_in_chat(
        chat_id=chat_id,
        message_id=message_id,
        keycloak_id=current_user.keycloak_id,
    )


@router.put("/{chat_id}/messages/{message_id}", response_model=MessageResponse)
async def update_message_in_chat(
    chat_id: UUID,
    message_id: UUID,
    body: MessageUpdate,
    service: MessageServiceDep,
    current_user: CurrentUserDep,
):
    return await service.update_message_in_chat(
        chat_id=chat_id,
        message_id=message_id,
        keycloak_id=current_user.keycloak_id,
        content=body.content,
    )


@router.delete(
    "/{chat_id}/messages/{message_id}", response_model=MessageResponse
)  # ONLY ADMIN
async def delete_message_in_chat(
    chat_id: UUID,
    message_id: UUID,
    service: MessageServiceDep,
    current_user: CurrentUserDep,
):
    return await service.delete_message_in_chat(
        chat_id=chat_id,
        message_id=message_id,
        keycloak_id=current_user.keycloak_id,
    )


@router.post("/{chat_id}/messages/{message_id}/read-by", response_model=list[UserRead])
async def get_users_who_read_message(  # see who has read the message
    chat_id: UUID,
    message_id: UUID,
    service: MessageServiceDep,
    current_user: CurrentUserDep,
):
    return await service.get_users_who_read_message(
        chat_id=chat_id,
        message_id=message_id,
        keycloak_id=current_user.keycloak_id,
    )
