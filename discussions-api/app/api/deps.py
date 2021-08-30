"""API Dependencies module."""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.repository.comment import CommentRepositoryMongo
from app.repository.topic import TopicRepositoryMongo
from app.usecase.comment import CommentUsecase
from app.usecase.topic import TopicUsecase
from config import settings


async def get_topic_usecase() -> TopicUsecase:
    """Get topic usecase."""
    return TopicUsecase(__get_topic_repo(), __get_comment_repo())


async def get_comment_usecase() -> CommentUsecase:
    """Get comment usecase."""
    return CommentUsecase(__get_topic_repo(), __get_comment_repo())


def __get_topic_repo() -> TopicRepositoryMongo:
    """Get topic repository."""
    return TopicRepositoryMongo(__get_mongodb())


def __get_comment_repo() -> CommentRepositoryMongo:
    """Get comment repository."""
    return CommentRepositoryMongo(__get_mongodb())


def __get_mongodb() -> AsyncIOMotorDatabase:
    """Get MongoDB database."""
    mongodb_client = AsyncIOMotorClient(settings.db_url)
    return mongodb_client[settings.db_name]
