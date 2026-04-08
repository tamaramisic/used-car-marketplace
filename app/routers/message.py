from fastapi import APIRouter, Depends
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from app.schemas.message import MessageCreate, MessageUpdate, MessageResponse
from app.services.message import MessageService
from app.dependencies import get_session, get_current_user


router = APIRouter(prefix="/messages")


@router.post("/", response_model=MessageResponse)
async def send_message(
    body: MessageCreate,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user),
):
    return await MessageService.send_message(
        session=session,
        sender_id=current_user.id,
        receiver_id=body.receiver_id,
        content=body.content
    )


@router.get("/{user_id}", response_model=list[MessageResponse])
async def get_conversation(
    user_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user),
):
    return await MessageService.get_conversation(
        session=session,
        user_id=current_user.id,
        other_user_id=user_id
    )


@router.get("/single/{message_id}", response_model=MessageResponse)
async def get_message(
    message_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user),
):
    return await MessageService.get_message(
        session=session,
        message_id=message_id,
        user_id=current_user.id,
    )


@router.patch("/{message_id}/read")
async def mark_as_read(
    message_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user),
):
    return await MessageService.mark_as_read(
        session=session,
        message_id=message_id,
        user_id=current_user.id
    )


@router.put("/{message_id}", response_model=MessageResponse)
async def update_message(
    message_id: UUID,
    body: MessageUpdate,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user),
):
    return await MessageService.update_message(
        session=session,
        message_id=message_id,
        user_id=current_user.id,
        content=body.content
    )


@router.delete("/{message_id}")
async def delete_message(
    message_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user),
):
    success = await MessageService.delete_message(
        session=session,
        message_id=message_id,
        user_id=current_user.id,
    )

    return {"success": success}