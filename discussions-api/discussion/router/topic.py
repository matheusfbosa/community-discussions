"""Router module."""

from typing import List
from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from discussion.model.topic import Topic, UpdateTopic

router = APIRouter()


@router.get("/", response_description="List all topics")
async def list_topics(request: Request):
    """List all topics."""
    topics: List[Topic] = await request.app.topic_usecase.find_all()
    return topics


@router.get("/{topic_id}", response_description="Get a single topic")
async def get_topic(topic_id: str, request: Request):
    """Get a single topic."""
    if (topic := await request.app.topic_usecase.get(topic_id)) is not None:
        return topic

    raise HTTPException(status_code=404, detail=f"topic {topic_id} not found")


@router.post("/", response_description="Create a new topic")
async def create_topic(request: Request, topic: Topic = Body(...)):
    """Create a new topic."""
    new_topic = jsonable_encoder(topic)
    created_topic = await request.app.topic_usecase.create(new_topic)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_topic)


@router.put("/{topic_id}", response_description="Update a topic")
async def update_topic(topic_id: str, request: Request, topic: UpdateTopic = Body(...)):
    """Update a topic."""
    # Cleaning up the request body
    topic = {k: v for k, v in topic.dict().items() if v is not None}

    if len(topic) >= 1:
        updated_topic: Topic = await request.app.topic_usecase.update(topic_id, topic)
        return updated_topic

    if (existing_topic := await request.app.topic_usecase.get(topic_id)) is not None:
        return existing_topic

    raise HTTPException(status_code=404, detail=f"topic {topic_id} not found")


@router.delete("/{topic_id}", response_description="Delete a topic")
async def delete_topic(topic_id: str, request: Request):
    """Delete a topic."""
    deleted: bool = await request.app.topic_usecase.delete(topic_id)
    if deleted:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"topic {topic_id} not found")
