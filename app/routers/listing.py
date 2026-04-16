from typing import List, Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status

from app.core.dependencies import (
    ListingRepositoryDep,
    CurrentUserDep,
    UserRepositoryDep,
)
from app.schemas.listing.listing_read import ListingRead
from app.schemas.listing.listing_save import ListingSave
from app.schemas.listing.listing_update import ListingUpdate
from app.services.listing import ListingService

router = APIRouter(prefix="/listings")


def get_listing_service(repo: ListingRepositoryDep) -> ListingService:
    return ListingService(repo)


ListingServiceDep = Annotated[ListingService, Depends(get_listing_service)]


@router.get("/", response_model=List[ListingRead])
async def find_all(listing_service: ListingServiceDep):
    list_of_listings = await listing_service.find_all()
    return list_of_listings


@router.get("/{listing_id}", response_model=ListingRead)
async def find_by_id(listing_id: UUID, listing_service: ListingServiceDep):
    return await listing_service.find_by(listing_id)


@router.post("/", response_model=ListingRead, status_code=status.HTTP_201_CREATED)
async def save(
    listing: ListingSave,
    listing_service: ListingServiceDep,
    current_user: CurrentUserDep,
    user_repo: UserRepositoryDep,
):
    return await listing_service.create(listing, current_user, user_repo)


@router.patch("/{listing_id}", response_model=ListingRead)
async def update(
    listing: ListingUpdate,
    listing_id: UUID,
    listing_service: ListingServiceDep,
    current_user: CurrentUserDep,
    user_repo: UserRepositoryDep,
):
    return await listing_service.update(listing_id, listing, current_user, user_repo)


@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(
    listing_id: UUID,
    listing_service: ListingServiceDep,
    current_user: CurrentUserDep,
    user_repo: UserRepositoryDep,
):
    await listing_service.delete_by_id(listing_id, current_user, user_repo)
