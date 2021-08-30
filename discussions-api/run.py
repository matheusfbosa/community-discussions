import uvicorn

from config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        reload=settings.debug_mode,
        port=settings.port,
    )
