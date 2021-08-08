"""Router module."""

from typing import List
from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from discussion.model.comment import Comment, UpdateComment

router = APIRouter()


@router.get("/", response_description="List all comments")
async def list_comments(request: Request):
    """List all comments."""
    comments: List[Comment] = await request.app.comment_usecase.find_all()
    return comments


@router.get("/{comment_id}", response_description="Get a single comment")
async def get_comment(comment_id: str, request: Request):
    """Get a single comment."""
    if (comment := await request.app.comment_usecase.get(comment_id)) is not None:
        return comment

    raise HTTPException(status_code=404, detail=f"comment {comment_id} not found")


@router.post("/", response_description="Create a new comment")
async def create_comment(request: Request, comment: Comment = Body(...)):
    """Create a new comment."""
    new_comment = jsonable_encoder(comment)
    created_comment = await request.app.comment_usecase.create(new_comment)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_comment)


@router.put("/{comment_id}", response_description="Update a comment")
async def update_comment(
    comment_id: str, request: Request, comment: UpdateComment = Body(...)
):
    """Update a comment."""
    # Cleaning up the request body
    comment = {k: v for k, v in comment.dict().items() if v is not None}

    if len(comment) >= 1:
        updated_comment: Comment = await request.app.comment_usecase.update(
            comment_id, comment
        )
        return updated_comment

    if (
        existing_comment := await request.app.comment_usecase.get(comment_id)
    ) is not None:
        return existing_comment

    raise HTTPException(status_code=404, detail=f"comment {comment_id} not found")


@router.delete("/{comment_id}", response_description="Delete a comment")
async def delete_comment(comment_id: str, request: Request):
    """Delete a comment."""
    deleted: bool = await request.app.comment_usecase.delete(comment_id)
    if deleted:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"comment {comment_id} not found")
