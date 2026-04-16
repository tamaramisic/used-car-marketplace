from uuid import UUID

from fastapi import status
from fastapi.exceptions import HTTPException
from ..repositories.comment import CommentRepository
from ..repositories.listing import ListingRepository
from ..repositories.user import UserRepository
from app.repositories.models.comment import Comment
from app.schemas.comment import BaseComment
from app.repositories.models.user import User


class CommentService:
    def __init__(
        self,
        comment_repo: CommentRepository,
        listing_repo: ListingRepository,
        user_repo: UserRepository,
    ):
        self.comment_repo = comment_repo
        self.listing_repo = listing_repo
        self.user_repo = user_repo

    async def find_all_comments(self) -> list[Comment]:
        return await self.comment_repo.find_all()

    async def find_comment_by_id(self, id: UUID) -> Comment:
        comment = await self.comment_repo.find_by(id)

        if comment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found",
            )

        return comment

    async def create_comment(
        self, listing_id: UUID, req_body: BaseComment, user: User
    ) -> Comment:
        if not req_body.content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Comment cannot be an empty string",
            )

        listing = await self.listing_repo.find_by(listing_id)

        if listing is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Listing doesn't exist",
            )

        current_user = await self.user_repo.find_by_keycloak_id(user.keycloak_id)

        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_BAD_REQUEST,
                detail="User doesn't exist",
            )

        new_comment = Comment(
            content=req_body.content,
            listing_fk=listing_id,
            user_fk=current_user.id,
        )

        return await self.comment_repo.create(new_comment)

    async def update_comment(
        self, comment_id: UUID, new_comment: dict
    ) -> Comment | None:
        return await self.comment_repo.update(comment_id, new_comment)

    async def delete_comment(self, id: UUID, user: User) -> bool:
        comment = await self.comment_repo.find_by(id)

        if comment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment doesn't exist",
            )

        current_user = await self.user_repo.find_by_keycloak_id(user.keycloak_id)

        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User doesn't exist",
            )

        if current_user.id != comment.user_fk:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Comment can delete only its owner!",
            )

        return await self.comment_repo.delete_by_id(comment)
