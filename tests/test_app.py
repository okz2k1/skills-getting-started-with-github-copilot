import uuid

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_duplicate_signup_is_rejected():
    email = f"duplicate-{uuid.uuid4().hex}@mergington.edu"
    first = client.post("/activities/Chess Club/signup?email=" + email)
    assert first.status_code == 200

    second = client.post("/activities/Chess Club/signup?email=" + email)
    assert second.status_code == 400
    assert second.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_email():
    email = f"remove-{uuid.uuid4().hex}@mergington.edu"
    signup = client.post("/activities/Chess Club/signup?email=" + email)
    assert signup.status_code == 200

    response = client.delete("/activities/Chess Club/participants/" + email)
    assert response.status_code == 200
    assert email not in client.get("/activities").json()["Chess Club"]["participants"]
