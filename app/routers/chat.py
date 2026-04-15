from uuid import UUID

from fastapi import APIRouter

from app.core.dependencies import MessageServiceDep, CurrentUserDep
from app.schemas.message import MessageResponse, MessageCreate

router = APIRouter(prefix="/chat")


@router.post("/create-message", response_model=MessageResponse)
async def create_message(
    message: MessageCreate,
    chat_id: UUID,
    service: MessageServiceDep,
    user: CurrentUserDep,
):
    return await service.send_message(
        sender_id=user.id, chat_id=chat_id, content=message.content
    )
    # chat id - docs - pass


@router.get("/messages", response_model=list[MessageResponse])
async def read_all_chat_messages(
    chat_id: int, service: MessageServiceDep, user: CurrentUserDep
):
    pass


# @router.get("/{user_id}", response_model=list[MessageResponse])
# async def get_conversation(
#     user_id: UUID,
#     service: MessageServiceDep,
#     current_user = Depends(get_current_user),
# ):
#     return await MessageService.get_conversation(
#         user_id=current_user.id,
#         other_user_id=user_id
#     )
#
#
# @router.get("/single/{message_id}", response_model=MessageResponse)
# async def get_message(
#     message_id: UUID,
#     service: MessageServiceDep,
#     current_user = Depends(get_current_user),
# ):
#     return await MessageService.get_message(
#         message_id=message_id,
#         user_id=current_user.id,
#     )
#
#
# @router.patch("/{message_id}/read")
# async def mark_as_read(
#     message_id: UUID,
#     service: MessageServiceDep,
#     current_user = Depends(get_current_user),
# ):
#     return await MessageService.mark_as_read(
#         message_id=message_id,
#         user_id=current_user.id
#     )
#
#
# @router.put("/{message_id}", response_model=MessageResponse)
# async def update_message(
#     message_id: UUID,
#     body: MessageUpdate,
#     service: MessageServiceDep,
#     current_user = Depends(get_current_user),
# ):
#     return await MessageService.update_message(
#         message_id=message_id,
#         user_id=current_user.id,
#         content=body.content
#     )
#
#
# @router.delete("/{message_id}")
# async def delete_message(
#     message_id: UUID,
#     service: MessageServiceDep,
#     current_user = Depends(get_current_user),
# ):
#     success = await MessageService.delete_message(
#         message_id=message_id,
#         user_id=current_user.id,
#     )
#
#     return {"success": success}
