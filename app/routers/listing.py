from fastapi import APIRouter, HTTPException

from app.dependencies import ListingServiceDep
from app.models.listing import Listing
from app.schemas.listing.listing_read import ListingRead
from app.schemas.listing.listing_save import ListingSave
from app.schemas.listing.listing_update import ListingUpdate

router = APIRouter(prefix="/listing")

@router.get("/all", response_model=ListingRead)
async def find_all(listing_service: ListingServiceDep):
    list_of_listings = listing_service.find_all()
    if not list_of_listings:
        raise HTTPException(status_code=404, detail="Empty list")
    return await list_of_listings

@router.get("/by-id", response_model=ListingRead)
async def find_by_id(listing_id: int, listing_service: ListingServiceDep):
    listing = listing_service.find_by(listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing with given id doesn't exist")
    return await listing

@router.post("/save", response_model=ListingSave)
async def save(listing: Listing, listing_service: ListingServiceDep):
    return await listing_service.save_or_update(listing)

@router.patch("/update", response_model=ListingUpdate)
async def save(listing: Listing, listing_service: ListingServiceDep):
    return await listing_service.save_or_update(listing)

@router.delete("/delete")
async def delete_by_id(listing_id: int, listing_service: ListingServiceDep):
    await listing_service.delete_by_id(listing_id)

