from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.repositories.listing import ListingRepository
from app.services.listing import ListingService

from .repositories.comment import CommentRepository
from .services.comment import CommentService

SessionDep = Annotated[AsyncSession, Depends(get_session)]

# listing repository dependency
async def get_listing_repo(session: SessionDep) -> ListingRepository:
    return ListingRepository(session)

ListingRepositoryDep = Annotated[ListingRepository, Depends(get_listing_repo)]

# listing service dependency
async def get_listing_service(repo: Annotated[ListingRepository, Depends(get_listing_repo)]) -> ListingService:
    return ListingService(repo)

ListingServiceDep = Annotated[ListingService, Depends(get_listing_service)]


#################################################
#######COMMENT DEPENDENCIES#######

def get_comment_repo(session: SessionDep):
    return CommentRepository(session)

CommentRepoDep = Annotated[CommentRepository, Depends(get_comment_repo)]

def get_comment_service(repo: CommentRepoDep):
    return CommentService(repo)

CommentServiceDep = Annotated[CommentService, Depends(get_comment_service)]

#################################################
