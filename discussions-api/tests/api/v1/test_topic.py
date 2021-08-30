from fastapi.testclient import TestClient


def test_list_topics(client: TestClient) -> None:
    response = client.get("/api/v1/topics")
    assert response.status_code == 200
