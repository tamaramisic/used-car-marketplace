from app.repositories.models import User
from app.repositories.user import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_or_get_user(self, current_user: User) -> User:
        user = await self.user_repository.find_by_keycloak_id(current_user.keycloak_id)

        if not user:
            return await self.user_repository.create(current_user)

        return user
