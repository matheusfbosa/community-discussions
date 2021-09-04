"""Base repository module."""

import abc
from typing import Any, Dict, List, Optional

from app.domain.comment import Comment
from app.domain.topic import Topic


class TopicRepository:
    """Topic repository base."""

    COLLECTION_NAME = "discussions"

    @abc.abstractmethod
    async def find(self, skip: int, limit: int) -> List[Topic]:
        """Find topics."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def search(
        self, query: List[Dict[str, Any]], term: str, skip: int, limit: int
    ) -> List[Any]:
        """Search for topics."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def get(self, topic_id: str) -> Optional[Topic]:
        """Get a topic."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def create(self, topic: Dict[str, Any]) -> str:
        """Create a topic."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def update(self, topic_id: str, topic: Dict[str, Any]) -> int:
        """Update a topic."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete(self, topic_id: str) -> int:
        """Delete a topic."""
        raise NotImplementedError()


class CommentRepository:
    """Comment repository base."""

    COLLECTION_NAME = "discussions"

    @abc.abstractmethod
    async def find_by_topic(
        self, topic_id: str, skip: int, limit: int
    ) -> List[Comment]:
        """Find comments by topic."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def get(self, topic_id: str, comment_id: str) -> Optional[Comment]:
        """Get a comment."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def create(self, comment: Dict[str, Any]) -> str:
        """Create a comment."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def update(
        self, topic_id: str, comment_id: str, comment: Dict[str, Any]
    ) -> int:
        """Update a comment."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete(self, topic_id: str, comment_id: str) -> int:
        """Delete a comment."""
        raise NotImplementedError()
