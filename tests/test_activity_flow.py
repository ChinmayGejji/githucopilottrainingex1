from urllib.parse import quote


def test_signup_then_unregister_flow(client):
    # Arrange
    activity_name = "Debate Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "flowstudent@mergington.edu"

    # Act
    signup_response = client.post(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )
    unregister_response = client.delete(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    participants = activities_response.json()[activity_name]["participants"]
    assert email not in participants
