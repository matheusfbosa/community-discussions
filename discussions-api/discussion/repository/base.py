"""Repository module."""

import abc
from typing import Any, Dict, List, Optional


class TopicRepository:
    """Topic repository base."""

    COLLECTION_NAME = "discussions"

    @abc.abstractmethod
    async def find(self, skip: int, limit: int) -> List[Any]:
        """Find topics."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def search(
        self, query: List[Dict[str, Any]], term: str, skip: int, limit: int
    ) -> List[Any]:
        """Search for topics."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def get(self, topic_id: str) -> Optional[Any]:
        """Get a topic by id."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def create(self, topic: Any) -> Any:
        """Create a topic."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def update(self, topic_id: str, topic: Any) -> Optional[Any]:
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
    async def find(self, skip: int, limit: int) -> List[Any]:
        """Find comments."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def find_by_topic(self, topic_id: str, skip: int, limit: int) -> List[Any]:
        """Find comments by topic."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def get(self, comment_id: str) -> Optional[Any]:
        """Get a comment by id."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def create(self, comment: Any) -> Any:
        """Create a comment."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def update(self, comment_id: str, entity: Any) -> Optional[Any]:
        """Update a comment."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete(self, comment_id: str) -> int:
        """Delete a comment."""
        raise NotImplementedError()
