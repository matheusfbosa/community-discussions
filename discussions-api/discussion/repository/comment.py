"""Repository module."""

from typing import Any, Optional, List

from discussion.repository.base import Repository
from discussion.model.comment import Comment, UpdateComment


class CommentRepository(Repository):
    """Comments repository."""

    DISCUSSION_TYPE = "comment"

    def __init__(self, mongo: Any) -> None:
        self.mongodb = mongo[CommentRepository.COLLECTION_NAME]

    async def find_all(self) -> List[Any]:
        """Find all comments."""
        comments: List[Any] = []
        for doc in await self.mongodb.find(
            {"type": CommentRepository.DISCUSSION_TYPE}
        ).to_list(length=100):
            comments.append(doc)
        return comments

    async def get(self, entity_id: str) -> Optional[Comment]:
        """Get comment by id."""
        if (
            comment := await self.mongodb.find_one(
                {"_id": entity_id, "type": CommentRepository.DISCUSSION_TYPE}
            )
        ) is not None:
            return comment

    async def create(self, entity: Comment) -> Comment:
        """Create comment."""
        created_comment: Comment = await self.mongodb.insert_one(entity)
        return created_comment

    async def update(self, entity_id: str, entity: UpdateComment) -> Optional[Comment]:
        """Update comment."""
        result = await self.mongodb.update_one({"_id": entity_id}, {"$set": entity})
        return result.modified_count

    async def delete(self, entity_id: str) -> int:
        """Delete comment."""
        result = await self.mongodb.delete_one({"_id": entity_id})
        return result.deleted_count
