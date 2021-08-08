"""Repository module."""

from typing import Any, Dict, List, Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from discussion.repository.base import Repository
from discussion.model.comment import Comment


class CommentRepository(Repository):
    """Comments repository."""

    DISCUSSION_TYPE = "comment"

    def __init__(self, mongodb_client: AsyncIOMotorClient) -> None:
        self.mongodb: AsyncIOMotorDatabase = mongodb_client[
            CommentRepository.COLLECTION_NAME
        ]

    async def find(self, skip=0, limit=10) -> List[Comment]:
        """Find comments."""
        cursor = self.mongodb.find({"type": CommentRepository.DISCUSSION_TYPE})
        cursor.skip(skip).limit(limit)
        comments: List[Comment] = []
        async for doc in cursor:
            comments.append(doc)
        return comments

    async def search(
        self, query: List[Dict[str, Any]], term: str = None, skip=0, limit=10
    ) -> List[Comment]:
        """Search for comments."""
        query.append({"type": CommentRepository.DISCUSSION_TYPE})
        if term:
            query.append({"$text": {"$search": term}})
            cursor = self.mongodb.find(
                {"$and": query},
                {"score": {"$meta": "textScore"}},
            )
            # Sorting results in ascending order by text score
            cursor.sort([("score", {"$meta": "textScore"})])
        else:
            cursor = self.mongodb.find({"$and": query})
        cursor.skip(skip).limit(limit)

        comments: List[Comment] = []
        async for doc in cursor:
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

    async def create(self, entity: Comment) -> Any:
        """Create comment."""
        created_comment = await self.mongodb.insert_one(entity)
        return created_comment

    async def update(self, entity_id: str, entity: Dict[str, Any]) -> Any:
        """Update comment."""
        result = await self.mongodb.update_one({"_id": entity_id}, {"$set": entity})
        return result.modified_count

    async def delete(self, entity_id: str) -> int:
        """Delete comment."""
        result = await self.mongodb.delete_one({"_id": entity_id})
        return result.deleted_count
