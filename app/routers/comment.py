from uuid import UUID
from fastapi import APIRouter, Depends, status
from app.core.dependencies import CommentServiceDep, CurrentUserDep, get_current_user
from ..schemas.comment import CommentCreate, CommentRead, CommentUpdate

router = APIRouter(tags=["Comment"])


@router.get(
    "/comments",
    response_model=list[CommentRead],
    dependencies=[Depends(get_current_user)],
)
async def get_all_comments(service: CommentServiceDep):
    return await service.find_all_comments()


@router.get("/comments/{comment_id}", response_model=CommentRead)
async def get_comment_by_id(comment_id: UUID, service: CommentServiceDep):
    return await service.find_comment_by_id(comment_id)


@router.post(
    "/listings/{listing_id}/comments",
    response_model=CommentRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_new_comment(
    listing_id: UUID,
    req_body: CommentCreate,
    user: CurrentUserDep,
    service: CommentServiceDep,
):
    comment = await service.create_comment(listing_id, req_body, user)
    return comment


@router.patch("/comments/{comment_id}", response_model=CommentRead)
async def edit_comment(
    comment_id: UUID,
    new_content: CommentUpdate,
    user: CurrentUserDep,
    service: CommentServiceDep,
):
    return await service.update_comment(comment_id, new_content, user)


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: UUID, user: CurrentUserDep, service: CommentServiceDep
):
    await service.delete_comment(comment_id, user)
