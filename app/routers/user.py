from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.dependencies import CurrentUserDep, UserRepositoryDep
from app.schemas.user_read import UserRead
from app.services.user import UserService

router = APIRouter(prefix="/users")


async def get_user_service(repo: UserRepositoryDep) -> UserService:
    return UserService(repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


@router.post("/me", response_model=UserRead)
async def create_or_get_user(user: CurrentUserDep, user_service: UserServiceDep):
    return await user_service.create_or_get_user(user)
