from fastapi.testclient import TestClient
from app import app


client = TestClient(app)


def test_update():
    # first, create new author
    create_resp = client.post(
        "/authors",
        json={
            "name": "John Doe",
            "bio": "fake biography",
            "birth_date": "1990-03-25",
        },
    )

    # then, update author with new field
    author_id = create_resp.json()["data"]["id"]
    body = {
        "name": "New John Doe",
        "bio": "new fake biography",
        "birth_date": "2000-04-20",
    }

    response = client.put(
        f"/authors/{author_id}",
        json=body,
    )

    content = response.json()
    assert content["data"]["name"] == body["name"]
    assert content["data"]["bio"] == body["bio"]
    assert content["data"]["birth_date"] == body["birth_date"]
    assert content["status"] == 200
    assert content["message"] == "Author updated successfully"
