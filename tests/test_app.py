from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def reset_activities():
    """Reset in-memory activity data to its original state for each test."""
    activities.clear()
    activities.update(
        {
            "Chess Club": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
            },
            "Programming Class": {
                "description": "Learn programming fundamentals and build software projects",
                "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                "max_participants": 20,
                "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
            },
            "Gym Class": {
                "description": "Physical education and sports activities",
                "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
                "max_participants": 30,
                "participants": ["john@mergington.edu", "olivia@mergington.edu"],
            },
        }
    )


def test_get_activities_returns_activity_list():
    # Arrange
    reset_activities()

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
    assert data["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]


def test_signup_for_activity_adds_participant():
    # Arrange
    reset_activities()
    email = "newstudent@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup?email=" + email)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in activities["Chess Club"]["participants"]


def test_signup_for_unknown_activity_returns_404():
    # Arrange
    reset_activities()

    # Act
    response = client.post("/activities/Unknown Club/signup?email=student@mergington.edu")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_email_is_rejected():
    # Arrange
    reset_activities()
    email = "michael@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup?email=" + email)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_delete_participant_unregisters_student():
    # Arrange
    reset_activities()
    email = "michael@mergington.edu"

    # Act
    response = client.delete("/activities/Chess Club/participants?email=" + email)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Chess Club"
    assert email not in activities["Chess Club"]["participants"]


def test_delete_unknown_participant_returns_404():
    # Arrange
    reset_activities()
    email = "notregistered@mergington.edu"

    # Act
    response = client.delete("/activities/Chess Club/participants?email=" + email)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
