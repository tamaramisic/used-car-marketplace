from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.database import get_session
from app.repositories.listing import ListingRepository
from app.repositories.message import MessageRepository
from app.repositories.chat import ChatRepository
from app.repositories.comment import CommentRepository
from app.repositories.user import UserRepository
from app.services.comment import CommentService
from app.repositories.models.user import User
from app.security.security import verify_token, map_token_to_user

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


def get_comment_service(
    comment_repo: CommentRepoDep,
    listing_repo: ListingRepositoryDep,
    user_repo: "UserRepositoryDep",
):
    return CommentService(comment_repo, listing_repo, user_repo)


CommentServiceDep = Annotated[CommentService, Depends(get_comment_service)]
#################################################


#######MESSAGE DEPENDENCIES#######
# message repository dependency
async def get_message_repo(session: SessionDep) -> MessageRepository:
    return MessageRepository(session)


MessageRepositoryDep = Annotated[MessageRepository, Depends(get_message_repo)]
#################################################


#######CHAT DEPENDENCIES#######
# message repository dependency
async def get_chat_repo(session: SessionDep) -> ChatRepository:
    return ChatRepository(session)


ChatRepositoryDep = Annotated[ChatRepository, Depends(get_chat_repo)]
#################################################


#######USER DEPENDENCIES#######
async def get_user_repo(session: SessionDep) -> UserRepository:
    return UserRepository(session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repo)]


#######CURRENT USER#######
async def get_current_user(payload: dict = Depends(verify_token)) -> User:
    return map_token_to_user(payload)


CurrentUserDep = Annotated[User, Depends(get_current_user)]
