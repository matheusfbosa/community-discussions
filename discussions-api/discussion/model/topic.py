"""Model module."""

from typing import Optional
import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class Topic(BaseModel):
    """Topic model."""

    updated: Optional[datetime]
    topic_id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    content: str = Field(...)
    created: datetime = Field(default_factory=datetime.now)
    discussion_type: str = Field(default="topic", alias="type")

    class Config:
        """Topic model configuration."""

        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "title": "Hey!",
                "content": "Can you help me please?",
            }
        }


class UpdateTopic(BaseModel):
    """Topic model for update."""

    title: Optional[str]
    content: Optional[str]
    updated: Optional[datetime] = Field(default_factory=datetime.now)

    class Config:
        """Topic model for update configuration."""

        schema_extra = {
            "example": {
                "title": "Hey!",
                "content": "Can you help me please?",
            }
        }
