"""Community Discussions module."""

from fastapi import FastAPI
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient

from config import settings

from discussion.repository.topic import TopicRepository
from discussion.repository.comment import CommentRepository
from discussion.usecase.topic import TopicUsecase
from discussion.usecase.comment import CommentUsecase
from discussion.router.topic import router as topic_router
from discussion.router.comment import router as comment_router

app = FastAPI()


@app.on_event("startup")
async def startup() -> None:
    """Starts up the app."""
    create_app()


@app.on_event("shutdown")
async def shutdown() -> None:
    """Shuts down the app."""
    app.mongodb_client.close()


def create_app() -> None:
    """Creates the app."""
    # Database
    app.mongodb_client = AsyncIOMotorClient(settings.db_url)
    app.mongodb = app.mongodb_client[settings.db_name]
    # Repositories
    topic_repo = TopicRepository(app.mongodb)
    comment_repo = CommentRepository(app.mongodb)
    # Usecases
    app.topic_usecase = TopicUsecase(topic_repo, comment_repo)
    app.comment_usecase = CommentUsecase(topic_repo, comment_repo)
    # Routers
    app.include_router(topic_router, tags=["Topics"], prefix="/topics")
    app.include_router(comment_router, tags=["Comments"], prefix="/comments")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        reload=settings.debug_mode,
        port=settings.port,
    )
