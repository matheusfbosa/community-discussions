"""Topic module."""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Topic(BaseModel):
    """Topic model."""

    topic_id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    content: str = Field(...)
    username: str = Field(...)
    discussion_type: str = Field(default="topic", alias="type")
    created: datetime = Field(default_factory=datetime.now)
    updated: Optional[datetime] = Field(default=None)

    class Config:
        """Pydantic config class."""

        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "title": "Hey!",
                "content": "Can you help me please?",
                "username": "John Doe",
            }
        }


class UpdateTopic(BaseModel):
    """Topic model for update."""

    title: Optional[str]
    content: Optional[str]
    updated: Optional[datetime] = Field(default_factory=datetime.now)

    class Config:
        """Pydantic config class."""

        schema_extra = {
            "example": {"title": "Hey!", "content": "Can you help me please?"}
        }
