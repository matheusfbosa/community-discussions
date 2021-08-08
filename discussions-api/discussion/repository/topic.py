"""Repository module."""

from typing import Any, Dict, List, Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from discussion.repository.base import Repository
from discussion.model.topic import Topic


class TopicRepository(Repository):
    """Topics repository."""

    DISCUSSION_TYPE = "topic"

    def __init__(self, mongodb_client: AsyncIOMotorClient) -> None:
        self.mongodb: AsyncIOMotorDatabase = mongodb_client[
            TopicRepository.COLLECTION_NAME
        ]

    async def find(self, skip: int, limit: int) -> List[Topic]:
        """Find topics."""
        cursor = self.mongodb.find({"type": TopicRepository.DISCUSSION_TYPE})
        cursor.skip(skip).limit(limit)
        topics: List[Topic] = []
        async for doc in cursor:
            topics.append(doc)
        return topics

    async def search(
        self,
        query: List[Dict[str, Any]],
        term: str = None,
        skip: int = 0,
        limit: int = 10,
    ) -> List[Topic]:
        """Search for topics."""
        query.append({"type": TopicRepository.DISCUSSION_TYPE})
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

        topics: List[Topic] = []
        async for doc in cursor:
            topics.append(doc)
        return topics

    async def get(self, entity_id: str) -> Optional[Topic]:
        """Get topic by id."""
        if (
            topic := await self.mongodb.find_one(
                {"_id": entity_id, "type": TopicRepository.DISCUSSION_TYPE}
            )
        ) is not None:
            return topic

    async def create(self, entity: Topic) -> Any:
        """Create topic."""
        created_topic = await self.mongodb.insert_one(entity)
        return created_topic

    async def update(self, entity_id: str, entity: Dict[str, Any]) -> Any:
        """Update topic."""
        result = await self.mongodb.update_one({"_id": entity_id}, {"$set": entity})
        return result.modified_count

    async def delete(self, entity_id: str) -> int:
        """Delete topic."""
        result = await self.mongodb.delete_one({"_id": entity_id})
        return result.deleted_count
