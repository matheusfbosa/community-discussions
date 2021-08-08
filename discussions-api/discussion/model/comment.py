"""Model module."""

from typing import Optional
import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class Comment(BaseModel):
    """Comment model."""

    comment_id: str = Field(default_factory=uuid.uuid4, alias="_id")
    topic_id: str = Field(..., alias="topic")
    content: str = Field(...)
    username: str = Field(...)
    discussion_type: str = Field(default="comment", alias="type")
    created: datetime = Field(default_factory=datetime.now)
    updated: Optional[datetime] = Field(default=None, alias="updated")
    reply_comment: Optional[str] = Field(default=None, alias="reply")

    class Config:
        """Comment model configuration."""

        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "topic": "665997b2-c769-48f5-a6b7-cd0a701c8d88",
                "content": "Sure! I can help you!",
                "username": "Nephew Bob",
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
