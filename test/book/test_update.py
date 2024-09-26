from fastapi.testclient import TestClient
from app import app


client = TestClient(app)


def test_update():
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

    create_resp = client.post(
        "/books",
        json={
            "author_id": author_resp.json()["data"]["id"],
            "title": "Good Book",
            "description": "fake description",
            "publish_date": "2010-05-28",
        },
    )

    # then, update book with new field
    book_id = create_resp.json()["data"]["id"]
    body = {
        "title": "New John Doe",
        "description": "new fake description",
        "publish_date": "2000-04-20",
    }

    response = client.put(
        f"/books/{book_id}",
        json=body,
    )

    content = response.json()
    assert content["data"]["title"] == body["title"]
    assert content["data"]["description"] == body["description"]
    assert content["data"]["publish_date"] == body["publish_date"]
    assert content["status"] == 200
    assert content["message"] == "Book updated successfully"
