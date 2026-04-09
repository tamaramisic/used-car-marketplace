from uuid import UUID
from ..repositories.comment import CommentRepository
from ..models.comment import Comment


class CommentService:
    def __init__(self, repo: CommentRepository):
        self.repo = repo

    async def find_all_comments(self) -> list[Comment]:
        return await self.repo.find_all()

    async def find_comment_by_id(self, id: UUID) -> Comment:
        return await self.repo.find_by(id)
    
    async def create_comment(self, comment: Comment) -> Comment:
        return await self.repo.create(comment)

    async def update_comment(self, comment_id: UUID, new_comment: dict) -> Comment | None:
        return await self.repo.update(comment_id, new_comment)
    
    async def delete_comment(self, id: UUID) -> bool:
        return await self.repo.delete_by_id(id)