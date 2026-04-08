from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.repositories.listing import ListingRepository
from app.services.listing import ListingService

SessionDep = Annotated[AsyncSession, Depends(get_session)]

# listing repository dependency
async def get_listing_repo(session: SessionDep) -> ListingRepository:
    return ListingRepository(session)

ListingRepositoryDep = Annotated[ListingRepository, Depends(get_listing_repo)]

# listing service dependency
async def get_listing_service(repo: Annotated[ListingRepository, Depends(get_listing_repo)]) -> ListingService:
    return ListingService(repo)

ListingServiceDep = Annotated[ListingService, Depends(get_listing_service)]


