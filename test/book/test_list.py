from fastapi.testclient import TestClient
from app import app


client = TestClient(app)


def test_list():
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

    # then, list all books
    book_id = create_resp.json()["data"]["id"]
    response = client.get(
        "/books",
    )

    content = response.json()
    for book in content["data"]:
        if book["id"] == book_id:
            assert book["title"] == body["title"]
            assert book["description"] == body["description"]
            assert book["publish_date"] == body["publish_date"]
            break

    assert content["status"] == 200
    assert content["message"] == "List book successfully"
