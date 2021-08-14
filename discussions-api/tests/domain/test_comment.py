"""Topic module test."""

import uuid
from datetime import datetime

from app.domain.comment import Comment


def test_comment_from_dict() -> None:
    """Test topic creation from dict."""
    data = {
        "_id": str(uuid.uuid4()),
        "topic": str(uuid.uuid4()),
        "reply": str(uuid.uuid4()),
        "content": "I can!",
        "username": "Ozzy Osbourne",
        "type": "comment",
        "created": datetime.now(),
        "updated": datetime.now(),
    }

    comment = Comment(**data)

    assert comment.comment_id == data["_id"]
    assert comment.topic_id == data["topic"]
    assert comment.reply_comment == data["reply"]
    assert comment.content == data["content"]
    assert comment.username == data["username"]
    assert comment.discussion_type == data["type"]
    assert comment.created == data["created"]
    assert comment.updated == data["updated"]
