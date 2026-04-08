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
    
    async def add_or_update_comment(self, comment: Comment) -> Comment:
        return await self.repo.save_or_update(comment)
    
    async def delete_comment(self, id: UUID):
        return await self.repo.delete_by_id(id)