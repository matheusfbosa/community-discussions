"""Repository module."""

from typing import Any, Optional, List

from discussion.repository.base import Repository
from discussion.model.topic import Topic, UpdateTopic


class TopicRepository(Repository):
    """Topics repository."""

    DISCUSSION_TYPE = "topic"

    def __init__(self, mongo: Any) -> None:
        self.mongodb = mongo[TopicRepository.COLLECTION_NAME]

    async def find_all(self) -> List[Any]:
        """Find all topics."""
        topics: List[Any] = []
        for doc in await self.mongodb.find(
            {"type": TopicRepository.DISCUSSION_TYPE}
        ).to_list(length=100):
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

    async def create(self, entity: Topic) -> Topic:
        """Create topic."""
        created_topic: Topic = await self.mongodb.insert_one(entity)
        return created_topic

    async def update(self, entity_id: str, entity: UpdateTopic) -> Optional[Topic]:
        """Update topic."""
        result = await self.mongodb.update_one({"_id": entity_id}, {"$set": entity})
        return result.modified_count

    async def delete(self, entity_id: str) -> int:
        """Delete topic."""
        result = await self.mongodb.delete_one({"_id": entity_id})
        return result.deleted_count
