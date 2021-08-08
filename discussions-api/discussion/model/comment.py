"""Model module."""

from typing import Optional
import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class Comment(BaseModel):
    """Comment model."""

    updated: Optional[datetime]
    comment_id: str = Field(default_factory=uuid.uuid4, alias="_id")
    topic_id: str = Field(..., alias="topic")
    content: str = Field(...)
    created: datetime = Field(default_factory=datetime.now)
    discussion_type: str = Field(default="comment", alias="type")

    class Config:
        """Comment model configuration."""

        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "topic": "665997b2-c769-48f5-a6b7-cd0a701c8d88",
                "content": "Sure! I can help you!",
            }
        }


class UpdateComment(BaseModel):
    """Comment model for update."""

    content: str = Field(...)
    updated: Optional[datetime] = Field(default_factory=datetime.now)

    class Config:
        """Comment model for update configuration."""

        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "content": "Sure! I can help you!",
            }
        }
