"""Repository module."""
import abc
from typing import Any, Dict, List, Optional


class Repository:
    """Base repository."""

    COLLECTION_NAME = "discussions"

    @abc.abstractmethod
    async def find(self, skip: int, limit: int) -> List[Any]:
        """Find entities."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def search(
        self, query: List[Dict[str, Any]], term: str, skip: int, limit: int
    ) -> List[Any]:
        """Search for entities."""
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
