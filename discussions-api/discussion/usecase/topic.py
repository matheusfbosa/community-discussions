"""Usecase module."""

from typing import Optional, List
from discussion.repository.topic import TopicRepository
from discussion.repository.comment import CommentRepository
from discussion.model.topic import Topic, UpdateTopic


class TopicUsecase:
    """Topics usecase."""

    def __init__(
        self, topic_repo: TopicRepository, comment_repo: CommentRepository
    ) -> None:
        self.topic_repo = topic_repo
        self.comment_repo = comment_repo

    async def find_all(self) -> List[Topic]:
        """Find all topics."""
        topics: List[Topic] = await self.topic_repo.find_all()
        return topics

    async def get(self, topic_id: str) -> Optional[Topic]:
        """Get a topic."""
        topic: Topic = await self.topic_repo.get(topic_id)
        return topic

    async def create(self, topic: Topic) -> Topic:
        """Create a topic."""
        new_topic = await self.topic_repo.create(topic)
        created_topic: Topic = await self.topic_repo.get(new_topic.inserted_id)
        return created_topic

    async def update(self, topic_id: str, topic: UpdateTopic) -> Optional[Topic]:
        """Update a topic."""
        modified_count = await self.topic_repo.update(topic_id, topic)
        if modified_count == 1:
            if (updated_topic := await self.get(topic_id)) is not None:
                return updated_topic

    async def delete(self, topic_id: str) -> bool:
        """Delete a topic."""
        deleted_count: int = await self.topic_repo.delete(topic_id)
        return deleted_count > 0
