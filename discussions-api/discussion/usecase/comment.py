"""Usecase module."""

from typing import List, Optional

from discussion.repository.topic import TopicRepository
from discussion.repository.comment import CommentRepository
from discussion.model.comment import Comment, UpdateComment


class CommentUsecase:
    """Comments usecase."""

    def __init__(
        self, topic_repo: TopicRepository, comment_repo: CommentRepository
    ) -> None:
        self.topic_repo = topic_repo
        self.comment_repo = comment_repo

    async def find(self, skip: int, limit: int) -> List[Comment]:
        """Find all comments."""
        comments: List[Comment] = await self.comment_repo.find(skip, limit)
        return comments

    async def get(self, comment_id: str) -> Optional[Comment]:
        """Get a comment."""
        comment = await self.comment_repo.get(comment_id)
        return comment

    async def create(self, comment: Comment) -> Optional[Comment]:
        """Create a comment."""
        new_comment = await self.comment_repo.create(comment)
        created_comment = await self.comment_repo.get(new_comment.inserted_id)
        return created_comment

    async def update(
        self, comment_id: str, comment: UpdateComment
    ) -> Optional[Comment]:
        """Update a comment."""
        # Cleaning up the request body
        comment_clean = {k: v for k, v in comment.dict().items() if v is not None}

        if len(comment_clean) >= 1:
            modified_count = await self.comment_repo.update(comment_id, comment_clean)
            if modified_count == 1:
                if (
                    updated_comment := await self.comment_repo.get(comment_id)
                ) is not None:
                    return updated_comment

        if (existing_comment := await self.comment_repo.get(comment_id)) is not None:
            return existing_comment

    async def delete(self, comment_id: str) -> bool:
        """Delete a comment."""
        deleted_count: int = await self.comment_repo.delete(comment_id)
        return deleted_count > 0
