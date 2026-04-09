from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette import status

from app.dependencies import ListingServiceDep
from app.schemas.listing.listing_read import ListingRead
from app.schemas.listing.listing_save import ListingSave
from app.schemas.listing.listing_update import ListingUpdate

router = APIRouter(prefix="/listing")

@router.get("/all", response_model=List[ListingRead])
async def find_all(listing_service: ListingServiceDep):
    list_of_listings = await listing_service.find_all()
    return list_of_listings

@router.get("/{listing_id}", response_model=ListingRead)
async def find_by_id(listing_id: UUID, listing_service: ListingServiceDep):
    listing = await listing_service.find_by(listing_id)
    if not listing:
        raise HTTPException(status_code=404,
                            detail={
                                "message": "Listing with given id not found",
                                "listing_id": str(listing_id)
                            }
                            )
    return listing

@router.post("/save", response_model=ListingRead, status_code=status.HTTP_201_CREATED)
async def save(listing: ListingSave, listing_service: ListingServiceDep):
    return await listing_service.create(listing)

@router.patch("/{listing_id}", response_model=ListingRead)
async def update(listing: ListingUpdate, listing_id: UUID, listing_service: ListingServiceDep):
    listing_updated = await listing_service.update(listing_id, listing)
    if not listing_updated:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Listing not found",
                "listing_id": str(listing_id),
            },
        )


@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(listing_id: UUID, listing_service: ListingServiceDep):
    deleted = await listing_service.delete_by_id(listing_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Listing not found",
                "listing_id": str(listing_id),
            },
        )

