import uuid

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_duplicate_signup_is_rejected():
    # Arrange
    email = f"duplicate-{uuid.uuid4().hex}@mergington.edu"

    # Act
    first_response = client.post("/activities/Chess Club/signup?email=" + email)
    second_response = client.post("/activities/Chess Club/signup?email=" + email)

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up for this activity"
    assert client.get("/activities").json()["Chess Club"]["participants"].count(email) == 1


def test_unregister_participant_removes_email():
    # Arrange
    email = f"remove-{uuid.uuid4().hex}@mergington.edu"

    # Act
    signup_response = client.post("/activities/Chess Club/signup?email=" + email)
    remove_response = client.delete("/activities/Chess Club/participants/" + email)
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert remove_response.status_code == 200
    assert email not in activities_response.json()["Chess Club"]["participants"]


def test_signup_for_missing_activity_returns_404():
    # Arrange
    email = f"missing-activity-{uuid.uuid4().hex}@mergington.edu"

    # Act
    response = client.post("/activities/Unknown Activity/signup?email=" + email)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
