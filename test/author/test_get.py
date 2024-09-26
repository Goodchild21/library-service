from fastapi.testclient import TestClient
from app import app


client = TestClient(app)


def test_get():
    # first, create new author
    body = {
        "name": "John Doe",
        "bio": "fake biography",
        "birth_date": "1990-03-25",
    }

    create_resp = client.post(
        "/authors",
        json=body,
    )

    # then, get author by id
    author_id = create_resp.json()["data"]["id"]
    response = client.get(
        f"/authors/{author_id}",
    )

    content = response.json()
    assert content["data"]["name"] == body["name"]
    assert content["data"]["bio"] == body["bio"]
    assert content["data"]["birth_date"] == body["birth_date"]
    assert content["status"] == 200
    assert content["message"] == "Get author successfully"
