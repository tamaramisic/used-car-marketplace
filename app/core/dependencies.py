from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.database import get_session
from app.repositories.listing import ListingRepository
from app.repositories.message import MessageRepository
from app.repositories.user import UserRepository
from app.services.message import MessageService
from app.repositories.models.user import User

from app.repositories.comment import CommentRepository
from app.security.security import verify_token, map_token_to_user
from app.services.comment import CommentService

SessionDep = Annotated[AsyncSession, Depends(get_session)]


############LISTING DEPENDENCIES###########
# listing repository dependency
async def get_listing_repo(session: SessionDep) -> ListingRepository:
    return ListingRepository(session)


ListingRepositoryDep = Annotated[ListingRepository, Depends(get_listing_repo)]


#################################################

#######COMMENT DEPENDENCIES#######


def get_comment_repo(session: SessionDep):
    return CommentRepository(session)


CommentRepoDep = Annotated[CommentRepository, Depends(get_comment_repo)]


def get_comment_service(repo: CommentRepoDep):
    return CommentService(repo)


CommentServiceDep = Annotated[CommentService, Depends(get_comment_service)]

#################################################

#######MESSAGE DEPENDENCIES#######


# message repository dependency
async def get_message_repo(session: SessionDep) -> MessageRepository:
    return MessageRepository(session)


MessageRepositoryDep = Annotated[MessageRepository, Depends(get_message_repo)]


# message service dependency
async def get_message_service(repo: MessageRepositoryDep) -> MessageService:
    return MessageService(repo)


MessageServiceDep = Annotated[MessageService, Depends(get_message_service)]

#################################################


#######CURRENT USER#######
async def get_current_user(payload: dict = Depends(verify_token)) -> User:
    return map_token_to_user(payload)


CurrentUserDep = Annotated[User, Depends(get_current_user)]


async def get_user_repo(session: SessionDep) -> UserRepository:
    return UserRepository(session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repo)]
