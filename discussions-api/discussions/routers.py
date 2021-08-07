from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .models import TopicModel, UpdateTopicModel

router = APIRouter()

COLLECTION = "discussions"


@router.post("/", response_description="Create a new topic")
async def create_topic(request: Request, topic: TopicModel = Body(...)):
    """Create a new topic."""
    topic = jsonable_encoder(topic)
    new_topic = await request.app.mongodb[COLLECTION].insert_one(topic)
    created_topic = await request.app.mongodb[COLLECTION].find_one(
        {"_id": new_topic.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_topic)


@router.get("/", response_description="List all topics")
async def list_topics(request: Request):
    """List all topics."""
    topics = []
    for doc in await request.app.mongodb[COLLECTION].find().to_list(length=100):
        topics.append(doc)
    return topics


@router.get("/{id}", response_description="Get a single topic")
async def get_topic(id: str, request: Request):
    """Get a single topic."""
    if (
        topic := await request.app.mongodb[COLLECTION].find_one({"_id": id})
    ) is not None:
        return topic

    raise HTTPException(status_code=404, detail=f"topic {id} not found")


@router.put("/{id}", response_description="Update a topic")
async def update_topic(id: str, request: Request, topic: UpdateTopicModel = Body(...)):
    """Update a topic."""
    topic = {k: v for k, v in topic.dict().items() if v is not None}

    if len(topic) >= 1:
        update_result = await request.app.mongodb[COLLECTION].update_one(
            {"_id": id}, {"$set": topic}
        )

        if update_result.modified_count == 1:
            if (
                updated_topic := await request.app.mongodb[COLLECTION].find_one(
                    {"_id": id}
                )
            ) is not None:
                return updated_topic

    if (
        existing_topic := await request.app.mongodb[COLLECTION].find_one({"_id": id})
    ) is not None:
        return existing_topic

    raise HTTPException(status_code=404, detail=f"topic {id} not found")


@router.delete("/{id}", response_description="Delete a topic")
async def delete_topic(id: str, request: Request):
    """Delete a topic."""
    delete_result = await request.app.mongodb[COLLECTION].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"topic {id} not found")
