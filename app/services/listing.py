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
        """
        Gets all listings as a list

        Returns:
        List of Listing sql model
        """
        return await self.repo.find_all()

    async def find_by(self, listing_id: UUID) -> Listing:
        """
        Gets Listing with the given id

        Args:
            listing_id: UUID of Listing sql model

        Returns:
            Listing sql model
        """
        listing = await self.repo.find_by(listing_id)
        if not listing:
            raise HTTPException(
                status_code=404, detail=f"Listing with {listing_id} not found"
            )

        return listing

    async def create(
        self, listing_schema: ListingSave, current_user: User, user_repo: UserRepository
    ) -> Listing:
        """
        Checks if listing with the given title(unique) provided in schema
        already exists and raises exception, if not creates new Listing

        Args:
            listing_schema: pydantic schema od Listing for save
            current_user: user dependency
            user_repo: user repository

        Returns:
            Listing sql model
        """
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
        """
        Sets manually each attribute in Listing as the provided
        ones in schema and updates the Listing

        Args:
            listing_id: UUID of Listing sql model
            listing_schema: pydantic schema of Listing for update
            current_user: user dependency
            user_repo: user repository

        Returns:
            Listing sql model
        """

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
        """
        Deletes listing with given listing id

        Args:
            listing_id: UUID of Listing sql model
            current_user: user dependency
            user_repo: user repository

        Returns:
            /
        """
        listing = await self.check_user_permission_for_listing(
            listing_id, current_user, user_repo
        )
        return await self.repo.delete_by_id(listing)

    async def check_user_permission_for_listing(
        self, listing_id, current_user: User, user_repo: UserRepository
    ) -> Listing:
        """
        Method check if logged in user is the one who created listing,
        if not then raise exception he can't delete other's listings,
        and check if logged in user is admin, then he can delete any listing

        Args:
            listing_id: UUID of Listing sql model
            current_user: user dependency
            user_repo: user repository

        Returns:
            Listing sql model
        """
        listing = await self.repo.find_by(listing_id)

        if not listing:
            raise HTTPException(
                status_code=404, detail=f"Listing with {listing_id} not found"
            )

        user = await user_repo.find_by_keycloak_id(current_user.keycloak_id)

        if listing.user_fk != user.id:
            # admin can delete everyone's listings
            if "admin" in current_user.roles:
                return listing

            raise HTTPException(
                status_code=403, detail="User can't delete other user's listings"
            )

        return listing
