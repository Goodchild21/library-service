from fastapi.testclient import TestClient
from app import app


client = TestClient(app)


def test_delete():
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

    # then, delete book
    book_id = create_resp.json()["data"]["id"]
    response = client.delete(
        f"/books/{book_id}",
    )

    content = response.json()
    assert content["status"] == 200
    assert content["message"] == "Book deleted successfully"
