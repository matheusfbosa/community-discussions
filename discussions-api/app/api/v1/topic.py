"""Topic router module."""

from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.domain.topic import Topic, UpdateTopic
from app.usecase.topic import TopicCanNotBeChanged

router = APIRouter()


@router.get("", response_description="List topics")
async def list_topics(
    request: Request, skip: int = 0, limit: int = 10
) -> List[Topic]:
    """List topics."""
    topics = await request.app.topic_usecase.find(skip, limit)
    return topics


@router.get("/search", response_description="Search for topics")
async def search_topics(
    request: Request, term: str, skip: int = 0, limit: int = 10
) -> List[Topic]:
    """Search for topics."""
    topics: List[Topic] = await request.app.topic_usecase.search(
        term, skip, limit
    )
    return topics


@router.get("/{topic_id}", response_description="Get a single topic")
async def get_topic(request: Request, topic_id: str) -> Optional[Topic]:
    """Get a single topic."""
    if (topic := await request.app.topic_usecase.get(topic_id)) is not None:
        return topic
    raise HTTPException(status_code=404, detail=f"topic {topic_id} not found")


@router.post("", response_description="Create a new topic")
async def create_topic(
    request: Request, topic: Topic = Body(...)
) -> JSONResponse:
    """Create a new topic."""
    created_topic = await request.app.topic_usecase.create(topic)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=created_topic
    )


@router.put("/{topic_id}", response_description="Update an existing topic")
async def update_topic(
    request: Request, topic_id: str, topic: UpdateTopic = Body(...)
) -> JSONResponse:
    """Update an existing topic."""
    try:
        if (
            updated_topic := await request.app.topic_usecase.update(
                topic_id, topic
            )
        ) is not None:
            return updated_topic
    except TopicCanNotBeChanged as err:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=str(err)
        )
    else:
        raise HTTPException(
            status_code=404, detail=f"topic {topic_id} not found"
        )


@router.delete("/{topic_id}", response_description="Delete a topic")
async def delete_topic(request: Request, topic_id: str) -> JSONResponse:
    """Delete a topic."""
    try:
        deleted: bool = await request.app.topic_usecase.delete(topic_id)
    except TopicCanNotBeChanged as err:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=str(err)
        )
    else:
        if deleted:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        raise HTTPException(
            status_code=404, detail=f"topic {topic_id} not found"
        )
