from typing import Optional
import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class TopicModel(BaseModel):
    """Topic model."""

    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    content: str = Field(...)
    created: datetime = Field(default_factory=datetime.now)
    updated: Optional[datetime]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "title": "Hey!",
                "content": "Can you help me please?",
                "created": "2021-08-07T10:20:30.123",
                "updated": "2021-08-07T10:20:35.123",
            }
        }


class UpdateTopicModel(BaseModel):
    """Update topic model."""

    title: Optional[str]
    content: Optional[str]
    updated: Optional[datetime] = Field(default_factory=datetime.now)

    class Config:
        schema_extra = {
            "example": {
                "title": "Hey!",
                "content": "Can you help me please?",
                "updated": "2021-08-07T10:20:35.123",
            }
        }
