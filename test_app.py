import pytest

from app import app, tasks


@pytest.fixture
def client():
    original_tasks = [task.copy() for task in tasks]
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client

    tasks.clear()
    tasks.extend(original_tasks)


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_create_task(client):
    response = client.post(
        "/tasks",
        json={"title": "Write tests"},
    )

    assert response.status_code == 201
    assert response.get_json()["title"] == "Write tests"


def test_reject_empty_title(client):
    response = client.post("/tasks", json={"title": " "})

    assert response.status_code == 400


def test_pagination(client):
    response = client.get("/tasks?page=1&limit=1")

    assert response.status_code == 200
    assert len(response.get_json()["items"]) == 1
    assert response.get_json()["page"] == 1


def test_reject_invalid_page(client):
    response = client.get("/tasks?page=0&limit=10")

    assert response.status_code == 400