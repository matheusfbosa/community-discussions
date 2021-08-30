"""Community discussions module."""

from fastapi import FastAPI

from app.api.v1.router import api_router_v1
from config import settings

app = FastAPI(
    title=settings.APP_NAME, openapi_url=f"{settings.API_V1}/openapi.json",
)
app.include_router(api_router_v1, prefix=settings.API_V1)
