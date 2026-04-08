from sqlalchemy.ext.asyncio import AsyncSession
from .base_repository import BaseRepository
from ..models.comment import Comment


class CommentRepository(BaseRepository[Comment]):
    def __init__(self, session: AsyncSession):
        super().__init__(Comment, session)