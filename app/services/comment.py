from uuid import UUID

from fastapi import status
from fastapi.exceptions import HTTPException
from ..repositories.comment import CommentRepository
from ..repositories.listing import ListingRepository
from ..repositories.user import UserRepository
from app.repositories.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate
from app.repositories.models.user import User
from .exceptions.comment import (
    CommentNotFound,
    NotCommentAuthorDelete,
    NotCommentAuthorUpdate,
)
from .exceptions.listing_not_found import ListingNotFound


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
        """
        Gets all comments from a database

        Returns:
        List of Comment sql model
        """

        return await self.comment_repo.find_all()

    async def find_comment_by_id(self, id: UUID) -> Comment:
        """
        Gets a Comment with the given id

        Args:
            id: UUID of Comment sql model

        Returns:
            Comment sql model
        """

        comment = await self.comment_repo.find_by(id)

        if comment is None:
            raise CommentNotFound()

        return comment

    async def create_comment(
        self, listing_id: UUID, req_body: CommentCreate, user: User
    ) -> Comment:
        """
        Checks if listing with the given id exists and raises exception if not, checks if user exists in our database and raises exception if not, creates new Comment if everything is ok

        Args:
            listing_id: UUID of the Listing for which the comment is being created
            req_body: pydantic schema of the Comment being created
            user: sql model of the User creating the coment

        Returns:
            Newly created Comment sql model
        """

        listing = await self.listing_repo.find_by(listing_id)

        if listing is None:
            raise ListingNotFound(listing_id)

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
        self, comment_id: UUID, new_content: CommentUpdate, user: User
    ) -> Comment:
        """
        Updates the content attribute of the comment with the passed id. Raises an exception if the comment doesn't exist. Only the author can update a comment

        Args:
            comment_id: UUID of the Comment for which the content is being updated
            new_content: pydantic schema of the Comment being updated
            user: sql model of the User updating the coment

        Returns:
            Comment sql model
        """

        comment = await self.comment_repo.find_by(comment_id)

        if comment is None:
            raise CommentNotFound()

        current_user = await self.user_repo.find_by_keycloak_id(user.keycloak_id)

        if comment.user_fk != current_user.id:
            raise NotCommentAuthorUpdate()

        comment.content = new_content.content

        return await self.comment_repo.update(comment)

    async def delete_comment(self, id: UUID, user: User) -> bool:
        """
        Checks if Comment exists with a given id, then deletes it from the database. Only the author can delete a comment.

        Args:
            id: UUID of the Comment being deleted
            user: sql model of the User deleting the coment

        Returns:
            /
        """

        comment = await self.comment_repo.find_by(id)

        if comment is None:
            raise CommentNotFound()

        current_user = await self.user_repo.find_by_keycloak_id(user.keycloak_id)

        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User doesn't exist",
            )

        if current_user.id != comment.user_fk:
            raise NotCommentAuthorDelete()

        return await self.comment_repo.delete(comment)
