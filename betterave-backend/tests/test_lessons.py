"""Tests for the lessons endpoints."""

# type: ignore
from datetime import date
import pytest
from betterave_backend.app.models import UserType, UserLevel
from betterave_backend.app.operations.user_operations import add_user
from betterave_backend.app.operations.lesson_operations import add_lesson
from betterave_backend.app.operations.class_group_operations import add_class_group
from betterave_backend.app.operations.class_operations import add_class

LESSON_ID = "lesson_2"
LESSON_DATE = date(2023, 12, 21)
START_TIME = "09:00"
END_TIME = "10:00"
STUDENT_NAME = ("Lucas", "Felix")
ROOM = "A10"


@pytest.fixture
def setup_admin(test_client) -> int:
    """Create a user and returns their ID."""
    admin_id = add_user("Directeur", "Admin", "teacher_pic_url", UserType.ADMIN, UserLevel.NA)
    return admin_id


@pytest.fixture
def setup_teacher(test_client) -> int:
    """Create a user and returns their ID."""
    teacher_id = add_user("John", "Martins", "teacher_pic_url", UserType.TEACHER, UserLevel.NA)
    return teacher_id


@pytest.fixture
def setup_class(test_client, setup_teacher) -> int:
    """Fixture to create a class and return its instance."""
    class_id = add_class(
        class_id=5,
        name="Test Class 2",
        ects_credits=3,
        default_teacher_id=setup_teacher,
        level="1A",
        background_color="#123456",
    )
    return class_id


@pytest.fixture
def setup_group(test_client, setup_class) -> int:
    """Create a group and return its instance."""
    group_id = add_class_group(
        name="Test Group",
        is_main_group=False,
        class_id=setup_class,
    )
    return group_id


@pytest.fixture
def setup_login_admin(test_client, setup_admin) -> int:
    """Login admin."""
    paylod_login = {"email": "directeur.admin@ensae.fr", "password": "dadmin"}

    response_login = test_client.post("/auth/login", json=paylod_login)
    return response_login


@pytest.fixture
def setup_lesson(test_client, setup_group, setup_teacher) -> int:
    """Create a lesson and return its instance."""
    lesson_id = add_lesson(
        group_id=setup_group,
        date=LESSON_DATE,
        start_time=START_TIME,
        end_time=END_TIME,
        homework=None,
        room=ROOM,
        teacher_id=setup_teacher,
    )
    return lesson_id


def test_get_all_lessons_route(test_client):
    """LessonList.GET should return 200."""
    response = test_client.get("/lessons/")
    assert response.status_code == 200


def test_post_lesson_route(test_client, setup_login_admin, setup_teacher):
    """LessonList.POST should return 201."""
    payload = {
        "group_id": 9740,
        "date": "2024-04-25",
        "start_time": START_TIME,
        "end_time": END_TIME,
        "room": "salle X",
        "teacher_id": setup_teacher,
        "homework": None,
    }
    response = test_client.post("/lessons/", json=payload)
    assert response.status_code == 201


def test_get_lesson_by_id_route(test_client, setup_lesson):
    """LessonResource.GET should return 200."""
    response = test_client.get(f"/lessons/{setup_lesson}")
    assert response.status_code == 200


def test_update_lesson_route(test_client, setup_login_admin, setup_lesson):
    """LessonResource.PUT should return 204."""
    payload = {
        "title": "Econometrics of New Competition",
    }
    response = test_client.put(f"/lessons/{setup_lesson}", json=payload)
    assert response.status_code == 204


def test_delete_lesson_route(test_client, setup_login_admin, setup_lesson):
    """LessonResource.DELETE should return 204."""
    response = test_client.delete(f"/lessons/{setup_lesson}")
    assert response.status_code == 204
