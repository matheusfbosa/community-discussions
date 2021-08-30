from fastapi.testclient import TestClient


def test_list_comments_by_topic(client: TestClient) -> None:
    response = client.get("/api/v1/topics/1/comments")
    assert response.status_code == 200
