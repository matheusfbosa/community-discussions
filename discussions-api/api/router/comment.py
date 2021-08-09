"""Router module."""

from typing import List

from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from discussion.domain.comment import Comment, UpdateComment

router = APIRouter()


@router.get("/comments", response_description="List comments")
async def list_comments(request: Request, skip: int = 0, limit: int = 10):
    """List comments."""
    comments: List[Comment] = await request.app.comment_usecase.find(skip, limit)
    return comments


@router.get("/topics/{topic_id}/comments", response_description="List comments")
async def list_comments_by_topic(
    request: Request, topic_id: str, skip: int = 0, limit: int = 10
):
    """List comments."""
    comments: List[Comment] = await request.app.comment_usecase.find_by_topic(
        topic_id, skip, limit
    )
    return comments


@router.get("/comments/{comment_id}", response_description="Get a single comment")
async def get_comment(request: Request, comment_id: str):
    """Get a single comment."""
    if (comment := await request.app.comment_usecase.get(comment_id)) is not None:
        return comment
    raise HTTPException(status_code=404, detail=f"comment {comment_id} not found")


@router.post("/comments", response_description="Create a new comment")
async def create_comment(request: Request, comment: Comment = Body(...)):
    """Create a new comment."""
    new_comment = jsonable_encoder(comment)
    created_comment = await request.app.comment_usecase.create(new_comment)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_comment)


@router.put("/comments/{comment_id}", response_description="Update an existing comment")
async def update_comment(
    request: Request, comment_id: str, comment: UpdateComment = Body(...)
):
    """Update an existing comment."""
    if (
        updated_topic := await request.app.topic_usecase.update(comment_id, comment)
    ) is not None:
        return updated_topic
    raise HTTPException(status_code=404, detail=f"comment {comment_id} not found")


@router.delete("/comments/{comment_id}", response_description="Delete a comment")
async def delete_comment(request: Request, comment_id: str):
    """Delete a comment."""
    deleted: bool = await request.app.comment_usecase.delete(comment_id)
    if deleted:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"comment {comment_id} not found")
