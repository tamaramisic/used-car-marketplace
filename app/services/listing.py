from typing import List
from uuid import UUID
from fastapi import HTTPException
from app.repositories.models import User
from app.repositories.models.listing import Listing
from app.repositories.listing import ListingRepository
from app.repositories.user import UserRepository
from app.schemas.listing.listing_save import ListingSave
from app.schemas.listing.listing_update import ListingUpdate


class ListingService:
    def __init__(self, repo: ListingRepository):
        self.repo = repo

    async def find_all(self) -> List[Listing]:
        return await self.repo.find_all()

    async def find_by(self, listing_id: UUID) -> Listing:
        listing = await self.repo.find_by(listing_id)
        if not listing:
            raise HTTPException(
                status_code=404, detail=f"Listing with {listing_id} not found"
            )

        return listing

    async def create(
        self, listing_schema: ListingSave, current_user: User, user_repo: UserRepository
    ) -> Listing:
        listing = await self.repo.find_by_title(listing_schema.title)

        if listing:
            raise HTTPException(
                status_code=400,
                detail=f"Listing with a title:{listing_schema.title} already exists!",
            )

        user = await user_repo.find_by_keycloak_id(current_user.keycloak_id)
        listing_model = Listing(**listing_schema.model_dump())
        listing_model.seller = user
        return await self.repo.create(listing_model)

    async def update(
        self,
        listing_id: UUID,
        listing_schema: ListingUpdate,
        current_user: User,
        user_repo: UserRepository,
    ) -> Listing:
        listing = await self.check_user_permission_for_listing(
            listing_id, current_user, user_repo
        )

        update_data = listing_schema.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(listing, key, value)
        return await self.repo.update(listing)

    async def delete_by_id(
        self, listing_id: UUID, current_user: User, user_repo: UserRepository
    ):
        listing = await self.check_user_permission_for_listing(
            listing_id, current_user, user_repo
        )
        return await self.repo.delete_by_id(listing)

    async def check_user_permission_for_listing(
        self, listing_id, current_user: User, user_repo: UserRepository
    ) -> Listing:
        listing = await self.repo.find_by(listing_id)

        if not listing:
            raise HTTPException(
                status_code=404, detail=f"Listing with {listing_id} not found"
            )

        user = await user_repo.find_by_keycloak_id(current_user.keycloak_id)

        if listing.user_fk != user.id:
            raise HTTPException(
                status_code=403, detail="User can't delete other user's listings"
            )

        return listing
