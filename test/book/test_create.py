from fastapi.testclient import TestClient
from app import app


client = TestClient(app)


def test_create():
    # create new author first before creating book
    author_body = {
        "name": "John Doe",
        "bio": "fake biography",
        "birth_date": "1990-03-25",
    }
    author_resp = client.post(
        "/authors",
        json=author_body,
    )

    body = {
        "author_id": author_resp.json()["data"]["id"],
        "title": "Good Book",
        "description": "fake description",
        "publish_date": "2010-05-28",
    }

    response = client.post(
        "/books",
        json=body,
    )

    content = response.json()
    assert content["data"]["title"] == body["title"]
    assert content["data"]["description"] == body["description"]
    assert content["data"]["publish_date"] == body["publish_date"]
    assert content["status"] == 201
    assert content["message"] == "Book created successfully"
