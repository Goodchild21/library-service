from fastapi.testclient import TestClient
from app import app


client = TestClient(app)


def test_list_books():
    # first, create new author
    author_body = {
        "name": "John Doe",
        "bio": "fake biography",
        "birth_date": "1990-03-25",
    }

    author_resp = client.post(
        "/authors",
        json=author_body,
    )

    # then, create new book associated with author
    author_id = author_resp.json()["data"]["id"]
    book_body = {
        "author_id": author_id,
        "title": "Good Book",
        "description": "fake_description",
        "publish_date": "2010-05-08",
    }

    book_resp = client.post(
        "/books",
        json=book_body,
    )

    # then, list all books by author id
    book_id = book_resp.json()["data"]["id"]
    response = client.get(
        f"/authors/{author_id}/books",
    )

    content = response.json()
    for book in content["data"]:
        if book["id"] == book_id:
            assert book["author_id"] == author_id
            assert book["title"] == book_body["title"]
            assert book["description"] == book_body["description"]
            assert book["publish_date"] == book_body["publish_date"]
            break

    assert content["status"] == 200
    assert content["message"] == "List book by author ID successfully"
