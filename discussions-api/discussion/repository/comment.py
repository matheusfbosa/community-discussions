"""Repository module."""

from typing import Any, Dict, List, Optional

from motor.motor_asyncio import AsyncIOMotorClient

from discussion.domain.comment import Comment
from discussion.repository.base import CommentRepository


class CommentRepositoryMongo(CommentRepository):
    """Comments repository MongoDB."""

    DISCUSSION_TYPE = "comment"

    def __init__(self, mongodb_client: AsyncIOMotorClient) -> None:
        self.mongodb = mongodb_client[CommentRepositoryMongo.COLLECTION_NAME]

    async def find_by_topic(self, topic_id: str, skip=0, limit=10) -> List[Comment]:
        """Find comments by topic."""
        cursor = self.mongodb.find(
            {"topic": topic_id, "type": CommentRepositoryMongo.DISCUSSION_TYPE}
        )
        cursor.skip(skip).limit(limit)
        comments: List[Comment] = []
        async for doc in cursor:
            comments.append(doc)
        return comments

    async def get(self, topic_id: str, comment_id: str) -> Optional[Comment]:
        """Get a comment."""
        if (
            comment := await self.mongodb.find_one(
                {
                    "_id": comment_id,
                    "topic": topic_id,
                    "type": CommentRepositoryMongo.DISCUSSION_TYPE,
                }
            )
        ) is not None:
            return comment

    async def create(self, comment: Dict[str, Any]) -> str:
        """Create a comment."""
        result = await self.mongodb.insert_one(comment)
        return result.inserted_id

    async def update(
        self, topic_id: str, comment_id: str, comment: Dict[str, Any]
    ) -> int:
        """Update a comment."""
        result = await self.mongodb.update_one(
            {"_id": comment_id, "topic": topic_id}, {"$set": comment}
        )
        return result.modified_count

    async def delete(self, topic_id: str, comment_id: str) -> int:
        """Delete a comment."""
        result = await self.mongodb.delete_one({"_id": comment_id, "topic": topic_id})
        return result.deleted_count
