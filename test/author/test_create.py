from fastapi.testclient import TestClient
from app import app


client = TestClient(app)


def test_create():
    body = {
        "name": "John Doe",
        "bio": "fake biography",
        "birth_date": "1990-03-25",
    }

    response = client.post(
        "/authors",
        json=body,
    )

    content = response.json()
    assert content["data"]["name"] == body["name"]
    assert content["data"]["bio"] == body["bio"]
    assert content["data"]["birth_date"] == body["birth_date"]
    assert content["status"] == 201
    assert content["message"] == "Author created successfully"
