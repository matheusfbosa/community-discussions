from fastapi import APIRouter

from app.api.v1 import comment, topic

api_router_v1 = APIRouter()
api_router_v1.include_router(topic.router, tags=["Topics"], prefix="/topics")
api_router_v1.include_router(
    comment.router, tags=["Comments"], prefix="/topics/{topic_id}/comments",
)
