"""Repository module."""

from typing import Any, Dict, List, Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from discussion.domain.comment import Comment
from discussion.repository.base import CommentRepository


class CommentRepositoryMongo(CommentRepository):
    """Comments repository MongoDB."""

    DISCUSSION_TYPE = "comment"

    def __init__(self, mongodb_client: AsyncIOMotorClient) -> None:
        self.mongodb: AsyncIOMotorDatabase = mongodb_client[
            CommentRepositoryMongo.COLLECTION_NAME
        ]

    async def find(self, skip=0, limit=10) -> List[Comment]:
        """Find comments."""
        cursor = self.mongodb.find({"type": CommentRepositoryMongo.DISCUSSION_TYPE})
        cursor.skip(skip).limit(limit)
        comments: List[Comment] = []
        async for doc in cursor:
            comments.append(doc)
        return comments

    async def find_by_topic(self, topic_id: str, skip=0, limit=10) -> List[Comment]:
        """Find comments by topic."""
        cursor = self.mongodb.find(
            {"type": CommentRepositoryMongo.DISCUSSION_TYPE, "topic": topic_id}
        )
        cursor.skip(skip).limit(limit)
        comments: List[Comment] = []
        async for doc in cursor:
            comments.append(doc)
        return comments

    async def get(self, comment_id: str) -> Optional[Comment]:
        """Get a comment by id."""
        if (
            comment := await self.mongodb.find_one(
                {"_id": comment_id, "type": CommentRepositoryMongo.DISCUSSION_TYPE}
            )
        ) is not None:
            return comment

    async def create(self, comment: Comment) -> Any:
        """Create a comment."""
        created_comment = await self.mongodb.insert_one(comment)
        return created_comment

    async def update(self, comment_id: str, entity: Dict[str, Any]) -> Any:
        """Update a comment."""
        result = await self.mongodb.update_one({"_id": comment_id}, {"$set": entity})
        return result.modified_count

    async def delete(self, comment_id: str) -> int:
        """Delete a comment."""
        result = await self.mongodb.delete_one({"_id": comment_id})
        return result.deleted_count
