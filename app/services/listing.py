from typing import List
from uuid import UUID

from app.models.listing import Listing
from app.repositories.listing import ListingRepository
from app.schemas.listing.listing_save import ListingSave
from app.schemas.listing.listing_update import ListingUpdate


class ListingService:
    def __init__(self, repo: ListingRepository):
        self.repo = repo

    async def find_all(self) -> List[Listing]:
       return await self.repo.find_all()

    async def find_by(self, listing_id: UUID) -> Listing | None:
       return await self.repo.find_by(listing_id)

    async def create(self, listing_schema: ListingSave) -> Listing:
        listing_model = Listing(**listing_schema.model_dump())
        return await self.repo.create(listing_model)

    async def update(self, listing_id: UUID, listing_schema: ListingUpdate) -> Listing | None:
        update_data = listing_schema.model_dump(exclude_unset=True)
        return await self.repo.update(listing_id, update_data)

    async def delete_by_id(self, listing_id: UUID) -> bool:
        return await self.repo.delete_by_id(listing_id)

#     TODO: add service for checking if logged in user is the user in listing, returns bool(if is then can delete listing)

