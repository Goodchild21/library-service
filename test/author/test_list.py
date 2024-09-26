from fastapi.testclient import TestClient
from app import app


client = TestClient(app)


def test_list():
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

    # then, list all authors
    author_id = create_resp.json()["data"]["id"]
    response = client.get(
        "/authors",
    )

    content = response.json()
    for author in content["data"]:
        if author["id"] == author_id:
            assert author["name"] == body["name"]
            assert author["bio"] == body["bio"]
            assert author["birth_date"] == body["birth_date"]
            break

    assert content["status"] == 200
    assert content["message"] == "List author successfully"
