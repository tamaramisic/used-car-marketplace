from typing import List
from uuid import UUID

from app.models.listing import Listing
from app.repositories.listing import ListingRepository


class ListingService:
    def __init__(self, repo: ListingRepository):
        self.repo = repo

    async def find_all(self) -> List[Listing]:
       return await self.repo.find_all()

    async def find_by(self, listing_id: UUID) -> Listing | None:
       return await self.repo.find_by(listing_id)

    async def save_or_update(self, model: Listing) -> Listing | None:
        return await self.repo.save_or_update(model)

    async def delete_by_id(self, listing_id: UUID):
        await self.repo.delete_by_id(listing_id)

