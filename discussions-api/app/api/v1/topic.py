"""Topic router module."""

from typing import List, Optional, Union

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.api import deps
from app.domain.topic import Topic, UpdateTopic
from app.usecase.topic import TopicCanNotBeChanged, TopicUsecase

router = APIRouter()


@router.get("", response_description="List topics")
async def list_topics(
    skip: int = 0,
    limit: int = 10,
    usecase: TopicUsecase = Depends(deps.get_topic_usecase),
) -> List[Topic]:
    """List topics."""
    topics = await usecase.find(skip, limit)
    return topics


@router.get("/search", response_description="Search for topics")
async def search_topics(
    term: str,
    skip: int = 0,
    limit: int = 10,
    usecase: TopicUsecase = Depends(deps.get_topic_usecase),
) -> List[Topic]:
    """Search for topics."""
    topics: List[Topic] = await usecase.search(term, skip, limit)
    return topics


@router.get("/{topic_id}", response_description="Get a single topic")
async def get_topic(
    topic_id: str, usecase: TopicUsecase = Depends(deps.get_topic_usecase)
) -> Optional[Topic]:
    """Get a single topic."""
    if (topic := await usecase.get(topic_id)) is not None:
        return topic
    raise HTTPException(status_code=404, detail=f"topic {topic_id} not found")


@router.post("", response_description="Create a new topic")
async def create_topic(
    topic: Topic = Body(...),
    usecase: TopicUsecase = Depends(deps.get_topic_usecase),
) -> JSONResponse:
    """Create a new topic."""
    created_topic = await usecase.create(topic)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=created_topic
    )


@router.put("/{topic_id}", response_description="Update an existing topic")
async def update_topic(
    topic_id: str,
    topic: UpdateTopic = Body(...),
    usecase: TopicUsecase = Depends(deps.get_topic_usecase),
) -> Union[Topic, JSONResponse]:
    """Update an existing topic."""
    try:
        if (
            updated_topic := await usecase.update(topic_id, topic)
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
async def delete_topic(
    topic_id: str, usecase: TopicUsecase = Depends(deps.get_topic_usecase)
) -> JSONResponse:
    """Delete a topic."""
    try:
        deleted: bool = await usecase.delete(topic_id)
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
