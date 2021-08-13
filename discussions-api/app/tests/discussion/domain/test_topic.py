"""Topic module test."""

import uuid
from datetime import datetime

from discussion.domain.topic import Topic


def test_topic_from_dict() -> None:
    """Test topic creation from dict."""
    data = {
        "_id": str(uuid.uuid4()),
        "title": "Please can someone help me?",
        "content": "I'm stuck.",
        "username": "Jimi Hendrix",
        "type": "topic",
        "created": datetime.now(),
        "updated": datetime.now(),
    }

    topic = Topic(**data)

    assert topic.topic_id == data["_id"]
    assert topic.title == data["title"]
    assert topic.content == data["content"]
    assert topic.username == data["username"]
    assert topic.discussion_type == data["type"]
    assert topic.created == data["created"]
    assert topic.updated == data["updated"]
