from urllib.parse import quote


def test_unregister_success_removes_student(client):
    # Arrange
    activity_name = "Basketball Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "alex@mergington.edu"

    # Act
    unregister_response = client.delete(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )
    activities_response = client.get("/activities")

    # Assert
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Unregistered {email} from {activity_name}"
    participants = activities_response.json()[activity_name]["participants"]
    assert email not in participants


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_not_signed_up_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "notenrolled@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
