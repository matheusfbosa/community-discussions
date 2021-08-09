"""Usecase module."""

from typing import List, Optional, Tuple

from discussion.domain.comment import Comment
from discussion.domain.topic import Topic, UpdateTopic
from discussion.repository.topic import TopicRepositoryMongo
from discussion.repository.comment import CommentRepositoryMongo


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
        """Get a topic."""
        topic = await self.topic_repo.get(topic_id)
        return topic

    async def __get_comments_by_topic(self, topic_id: str) -> Tuple[List[Comment], int]:
        """Get comments by topic."""
        comments: List[Comment] = await self.comment_repo.find_by_topic(
            topic_id=topic_id, limit=100
        )
        return comments, len(comments)

    async def create(self, topic: Topic) -> Optional[Topic]:
        """Create a topic."""
        new_topic = await self.topic_repo.create(topic)
        created_topic = await self.topic_repo.get(new_topic.inserted_id)
        return created_topic

    async def update(self, topic_id: str, topic: UpdateTopic) -> Optional[Topic]:
        """Update a topic."""
        # Cleaning up the request body
        topic_clean = {k: v for k, v in topic.dict().items() if v is not None}

        if len(topic_clean) >= 1:
            # Check if the topic is not referenced by any comment
            _, comments_count = await self.__get_comments_by_topic(topic_id)
            if comments_count > 0:
                raise RuntimeError(
                    f"Can't update topic {topic_id}! It is referenced by {comments_count} comments."
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
            raise RuntimeError(
                f"Can't delete topic {topic_id}! It is referenced by {comments_count} comments."
            )
        deleted_count: int = await self.topic_repo.delete(topic_id)
        return deleted_count > 0
