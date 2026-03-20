import copy

from fastapi.testclient import TestClient
from src.app import app, activities

DEFAULT_ACTIVITIES = copy.deepcopy(activities)


def reset_activities():
    activities.clear()
    activities.update(copy.deepcopy(DEFAULT_ACTIVITIES))


client = TestClient(app)


def test_get_activities_returns_200_and_data():
    # Arrange
    reset_activities()

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity_success():
    # Arrange
    reset_activities()
    email = "newstudent@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert email in activities[activity]["participants"]


def test_signup_existing_participant_returns_400():
    # Arrange
    reset_activities()
    activity = "Chess Club"
    existing = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={existing}")

    # Assert
    assert response.status_code == 400


def test_signup_full_activity_returns_400():
    # Arrange
    reset_activities()
    activity_name = "Chess Club"
    activities[activity_name]["participants"] = [
        f"user{i}@mergington.edu" for i in range(activities[activity_name]["max_participants"])
    ]

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email=overflow@mergington.edu")

    # Assert
    assert response.status_code == 400


def test_remove_participant_success():
    # Arrange
    reset_activities()
    activity = "Chess Club"
    participant = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/participants/{participant}")

    # Assert
    assert response.status_code == 200
    assert participant not in activities[activity]["participants"]


def test_remove_participant_not_found_returns_404():
    # Arrange
    reset_activities()
    activity = "Chess Club"
    participant = "ghost@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/participants/{participant}")

    # Assert
    assert response.status_code == 404
