"""Tests for the events endpoints."""

# type: ignore
import pytest
from betterave_backend.app.operations.event_operations import add_event
from betterave_backend.app.models import UserType, UserLevel
from betterave_backend.app.operations.user_operations import add_user
from datetime import date

EVENT_ID = "event_1"
ASSO_ID = 30
EVENT_DATE = str(date(2024, 10, 20))
START_TIME = "09:00"
END_TIME = "10:00"
DESCRIPTION = "Test Réunion"
LOCATION = "Amphi 200"
PARTICIPANT_TYPE = "All users"


@pytest.fixture
def setup_admin(test_client) -> int:
    """Create a user and returns their ID."""
    admin_id = add_user("Directeur", "Admin", "teacher_pic_url", UserType.ADMIN, UserLevel.NA)
    return admin_id


@pytest.fixture
def setup_student(test_client) -> int:
    """Create a user and returns their ID."""
    student_id = add_user("Alice", "Martins", "student_pic_url", UserType.STUDENT, UserLevel._2A)
    return student_id


@pytest.fixture
def setup_login_admin(test_client, setup_admin) -> int:
    """Login admin."""
    paylod_login = {"email": "directeur.admin@ensae.fr", "password": "dadmin"}

    response_login = test_client.post("/auth/login", json=paylod_login)
    return response_login


@pytest.fixture
def setup_asso(test_client) -> int:
    """Create an asso user and returns their ID."""
    asso_id = add_user("BDS", "", "asso_pic_url", UserType.ASSO, UserLevel.NA)
    return asso_id


@pytest.fixture
def setup_event(test_client, setup_asso) -> int:
    """Fixture to create an event and return its instance."""
    event_id = add_event(
        asso_id=setup_asso,
        name="BDS - Réunion",
        date=EVENT_DATE,
        start_time=START_TIME,
        end_time=END_TIME,
        participants=PARTICIPANT_TYPE,
        description=DESCRIPTION,
        location=LOCATION,
    )
    return event_id


def test_get_event_route(test_client):
    """EventList.GET should return 200."""
    response = test_client.get("/events/")
    assert response.status_code == 200


def test_post_event_route(test_client, setup_asso, setup_login_admin):
    """EventList.POST should return 201 if the event is posted."""
    payload = {
        "asso_id": setup_asso,
        "name": "EJE - Réunion",
        "date": EVENT_DATE,
        "start_time": START_TIME,
        "end_time": END_TIME,
        "description": "réunion de l'asso EJE",
        "location": "Amphi 250",
        "participants": "All users",
    }

    response = test_client.post("/events/", json=payload)
    assert response.status_code == 201


def test_post_event_attendees_route(test_client, setup_login_admin, setup_student, setup_event):
    """EventAttendees.POST should return 200 if the attendees are posted."""
    payload = {"user_ids": [setup_student]}
    response = test_client.post(f"/events/{setup_event}/attendees", json=payload)
    assert response.status_code == 200


def test_delete_event_route(test_client, setup_login_admin, setup_event):
    """EventResource.DELETE should return 200 if the event is deleted."""
    response = test_client.delete(f"/events/{setup_event}")
    assert response.status_code == 200
