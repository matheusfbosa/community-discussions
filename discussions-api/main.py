"""Community Discussions module."""

import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.v1 import comment, topic
from config import settings
from app.discussion.repository.comment import CommentRepositoryMongo
from app.discussion.repository.topic import TopicRepositoryMongo
from app.discussion.usecase.comment import CommentUsecase
from app.discussion.usecase.topic import TopicUsecase

app = FastAPI(title=settings.app_name)
app.include_router(topic.router, tags=["Topics"], prefix="/v1/api/topics")
app.include_router(
    comment.router, tags=["Comments"], prefix="/v1/api/topics/{topic_id}/comments"
)

# Database
app.mongodb_client = AsyncIOMotorClient(settings.db_url)
app.mongodb = app.mongodb_client[settings.db_name]
# Repositories
topic_repo = TopicRepositoryMongo(app.mongodb)
comment_repo = CommentRepositoryMongo(app.mongodb)
# Usecases
app.topic_usecase = TopicUsecase(topic_repo, comment_repo)
app.comment_usecase = CommentUsecase(topic_repo, comment_repo)


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=settings.host, reload=settings.debug_mode, port=settings.port,
    )
