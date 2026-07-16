from urllib.parse import quote

from src import app as app_module


def test_get_activities_returns_all_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    body = response.json()
    assert "Chess Club" in body
    assert body["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_adds_student_to_activity(client):
    activity_name = quote("Chess Club", safe="")
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}
    assert email in app_module.activities["Chess Club"]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    response = client.post(
        f"/activities/{quote('Unknown Club', safe='')}/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_returns_400_for_duplicate_student(client):
    response = client.post(
        f"/activities/{quote('Chess Club', safe='')}/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student already signed up for this activity"
    }


def test_unregister_removes_student_from_activity(client):
    activity_name = quote("Basketball Team", safe="")
    email = "james@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Basketball Team"}
    assert email not in app_module.activities["Basketball Team"]["participants"]


def test_unregister_returns_404_for_missing_participant(client):
    response = client.delete(
        f"/activities/{quote('Basketball Team', safe='')}/signup",
        params={"email": "missing@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found"}