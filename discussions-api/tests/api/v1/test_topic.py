from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_list_topics():
    response = client.get("/v1/api/topics")
    assert response.status_code == 200
