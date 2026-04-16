from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.repositories.base_repository import BaseRepository
from app.repositories.models import User


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def find_by_keycloak_id(self, k_id: UUID) -> User | None:
        result = await self.db.execute(select(User).where(User.keycloak_id == k_id))
        return result.scalar_one_or_none()
