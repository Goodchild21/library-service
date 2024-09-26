from fastapi.testclient import TestClient
from app import app


client = TestClient(app)


def test_get():
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

    create_resp = client.post(
        "/books",
        json=body,
    )

    # then, get book by id
    book_id = create_resp.json()["data"]["id"]
    response = client.get(
        f"/books/{book_id}",
    )

    content = response.json()
    assert content["data"]["title"] == body["title"]
    assert content["data"]["description"] == body["description"]
    assert content["data"]["publish_date"] == body["publish_date"]
    assert content["status"] == 200
    assert content["message"] == "Get book successfully"
