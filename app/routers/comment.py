from uuid import UUID
from fastapi import APIRouter
from ..dependencies import CommentServiceDep
from ..schemas.comment import CommentCreate, CommentRead

router = APIRouter(prefix="/comments")

@router.get("/", response_model=CommentRead)
async def get_all_comments(service: CommentServiceDep):
    return await service.find_all_comments()

@router.get(f"/{id}", response_model=CommentRead)
async def get_comment_by_id(id: UUID, service: CommentServiceDep):
    return await service.find_comment_by_id(id)

@router.post()
async def add_new_comment():
    pass