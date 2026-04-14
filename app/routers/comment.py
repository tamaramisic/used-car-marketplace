from uuid import UUID
from fastapi import APIRouter
from app.core.dependencies import CommentServiceDep
from ..schemas.comment import CommentRead

router = APIRouter()


@router.get("/comments", response_model=CommentRead)
async def get_all_comments(service: CommentServiceDep):
    return await service.find_all_comments()


@router.get("/comments/{comment_id}", response_model=CommentRead)
async def get_comment_by_id(comment_id: UUID, service: CommentServiceDep):
    return await service.find_comment_by_id(comment_id)


@router.post("/listings/{listing_id}/comments")
async def add_new_comment(listing_id: UUID, service: CommentServiceDep):
    pass
