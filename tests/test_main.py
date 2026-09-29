from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_hello_returns_expected_message() -> None:
    response = client.get("/hello")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello World 2"}