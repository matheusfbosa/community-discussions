from fastapi import FastAPI
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

from discussions.routers import router

app = FastAPI()


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.db_url)
    app.mongodb = app.mongodb_client[settings.db_name]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(router, tags=[settings.app_name], prefix="/topics")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        reload=settings.debug_mode,
        port=settings.port,
    )
