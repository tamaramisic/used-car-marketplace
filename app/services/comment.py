from uuid import UUID

from fastapi import status
from fastapi.exceptions import HTTPException
from ..repositories.comment import CommentRepository
from app.repositories.models.comment import Comment
from app.schemas.comment import BaseComment
from app.repositories.models.user import User


class CommentService:
    def __init__(self, repo: CommentRepository):
        self.repo = repo

    async def find_all_comments(self) -> list[Comment]:
        return await self.repo.find_all()

    async def find_comment_by_id(self, id: UUID) -> Comment:
        return await self.repo.find_by(id)

    async def create_comment(
        self, listing_id: UUID, req_body: BaseComment, user: User
    ) -> Comment:
        # print({"listing_id: ": listing_id, "req_body": req_body, "username": user.username})
        if not req_body.content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Comment cannot be an empty string",
            )

        # how to check if listing_id is present in db with which repo?
        # how to find user with his keycloak id and then use user_fk as user id returned from the db

        new_comment = Comment(
            content=req_body.content,
            listing_fk=listing_id,
            user_fk=UUID("c2c3e855-f8b3-4e53-ad98-e082da01ea41"),
        )

        return await self.repo.create(new_comment)

    async def update_comment(
        self, comment_id: UUID, new_comment: dict
    ) -> Comment | None:
        return await self.repo.update(comment_id, new_comment)

    async def delete_comment(self, id: UUID) -> bool:
        return await self.repo.delete_by_id(id)
