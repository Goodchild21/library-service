from fastapi.testclient import TestClient
from app import app


client = TestClient(app)


def test_delete():
    # first, create new author
    create_resp = client.post(
        "/authors",
        json={
            "name": "John Doe",
            "bio": "fake biography",
            "birth_date": "1990-03-25",
        },
    )

    # then, delete author
    author_id = create_resp.json()["data"]["id"]
    response = client.delete(
        f"/authors/{author_id}",
    )

    content = response.json()
    assert content["status"] == 200
    assert content["message"] == "Author deleted successfully"
