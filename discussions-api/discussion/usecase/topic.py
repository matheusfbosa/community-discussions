"""Usecase module."""

from typing import List, Optional, Tuple

from fastapi.encoders import jsonable_encoder

from discussion.repository.topic import TopicRepositoryMongo
from discussion.repository.comment import CommentRepositoryMongo
from discussion.domain.comment import Comment
from discussion.domain.topic import Topic, UpdateTopic


class TopicCanNotBeChanged(Exception):
    """Custom error that is raised when a topic can not be changed."""

    def __init__(self, topic: str, comments_count: int, message: str) -> None:
        self.topic = topic
        self.comments_count = comments_count
        self.message = message
        super().__init__(message)


class TopicUsecase:
    """Topics usecase."""

    def __init__(
        self, topic_repo: TopicRepositoryMongo, comment_repo: CommentRepositoryMongo
    ) -> None:
        self.topic_repo = topic_repo
        self.comment_repo = comment_repo

    async def find(self, skip: int, limit: int) -> List[Topic]:
        """Find all topics."""
        topics: List[Topic] = await self.topic_repo.find(skip, limit)
        return topics

    async def search(self, term: str, skip: int, limit: int) -> List[Topic]:
        """Search for topics."""
        topics: List[Topic] = await self.topic_repo.search(
            query=[], term=term, skip=skip, limit=limit
        )
        return topics

    async def get(self, topic_id: str) -> Optional[Topic]:
        """Get a single topic."""
        topic = await self.topic_repo.get(topic_id)
        return topic

    async def create(self, topic: Topic) -> Optional[Topic]:
        """Create a topic."""
        inserted_id = await self.topic_repo.create(jsonable_encoder(topic))
        created_topic = await self.topic_repo.get(inserted_id)
        return created_topic

    async def update(self, topic_id: str, topic: UpdateTopic) -> Optional[Topic]:
        """Update a topic."""
        # Cleaning up the request body
        topic_clean = {k: v for k, v in topic.dict().items() if v is not None}

        if len(topic_clean) >= 1:
            # Check if the topic is not referenced by any comment
            _, comments_count = await self.__get_comments_by_topic(topic_id)
            if comments_count > 0:
                raise TopicCanNotBeChanged(
                    topic=topic_id,
                    comments_count=comments_count,
                    message="can not update topic referenced by one or more comments",
                )
            modified_count = await self.topic_repo.update(topic_id, topic_clean)
            if modified_count == 1:
                if (updated_topic := await self.topic_repo.get(topic_id)) is not None:
                    return updated_topic

        if (existing_topic := await self.topic_repo.get(topic_id)) is not None:
            return existing_topic

    async def delete(self, topic_id: str) -> bool:
        """Delete a topic."""
        # Check if the topic is not referenced by any comment
        _, comments_count = await self.__get_comments_by_topic(topic_id)
        if comments_count > 0:
            raise TopicCanNotBeChanged(
                topic=topic_id,
                comments_count=comments_count,
                message="can not delete topic referenced by one or more comments",
            )
        deleted_count: int = await self.topic_repo.delete(topic_id)
        return deleted_count > 0

    async def __get_comments_by_topic(self, topic_id: str) -> Tuple[List[Comment], int]:
        """Get comments by topic."""
        comments: List[Comment] = await self.comment_repo.find_by_topic(
            topic_id=topic_id, limit=100
        )
        return comments, len(comments)
