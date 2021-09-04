from typing import Generator

import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.main import app
from config import settings


@pytest.fixture(scope="session")
def db() -> Generator:
    mongodb_client = AsyncIOMotorClient(settings.db_url)
    yield mongodb_client[settings.db_name]


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
