from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.repositories.models.listing import Listing
from app.repositories.base_repository import BaseRepository


class ListingRepository(BaseRepository[Listing]):
    def __init__(self, db: AsyncSession):
        super().__init__(Listing, db)

    async def find_by_title(self, title) -> Listing:
        result = await self.db.execute(select(Listing).where(Listing.title == title))
        return result.scalar_one_or_none()
