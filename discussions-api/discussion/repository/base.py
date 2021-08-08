"""Repository module."""
import abc
from typing import Any, Optional


class Repository:
    """Base repository."""

    COLLECTION_NAME = "discussions"

    @abc.abstractmethod
    async def find_all(self) -> Any:
        """Find all entities."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def get(self, entity_id: str) -> Optional[Any]:
        """Get an entity."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def create(self, entity: Any) -> Any:
        """Create an entity."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def update(self, entity_id: str, entity: Any) -> Optional[Any]:
        """Update an entity."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete(self, entity_id: str) -> int:
        """Delete an entity."""
        raise NotImplementedError()
