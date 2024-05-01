"""Tests for the class_groups endpoints."""

# type: ignore
import pytest
from betterave_backend.app.operations.class_group_operations import add_class_group
from betterave_backend.app.operations.user_operations import add_user
from betterave_backend.app.operations.class_operations import add_class
from betterave_backend.app.models import UserType, UserLevel

# Constants for the test
CLASS_ID = 1
CLASS_NAME = "Test Class 2"
LEVEL = "1A"
ECTS_CREDITS = 3
BACKGROUND_COLOR = "#123456"


@pytest.fixture
def setup_teacher(test_client) -> int:
    """Create a user and returns their ID."""
    teacher_id = add_user("John", "Martins", "teacher_pic_url", user_type=UserType.TEACHER, level=UserLevel.NA)
    return teacher_id


@pytest.fixture
def setup_login_teacher(test_client, setup_teacher) -> int:
    """Login teacher."""
    paylod_login = {"email": "john.martins@ensae.fr", "password": "jmartins"}

    response_login = test_client.post("/auth/login", json=paylod_login)
    return response_login


@pytest.fixture
def setup_class(test_client, setup_teacher) -> int:
    """Fixture to create a class and return its instance."""
    class_id = add_class(
        class_id=CLASS_ID,
        name=CLASS_NAME,
        ects_credits=ECTS_CREDITS,
        default_teacher_id=setup_teacher,
        level=LEVEL,
        background_color=BACKGROUND_COLOR,
    )
    return class_id


@pytest.fixture
def setup_class_group(test_client, setup_class) -> int:
    """Fixture to create a class group within the setup class and return its ID."""
    group_id = add_class_group(name="TP 8", class_id=setup_class, is_main_group=False)
    return group_id


def test_get_class_groups_route(test_client):
    """ClassGroupList.GET should return 200."""
    response = test_client.get("/class_groups/")
    assert response.status_code == 200


def test_post_class_group_route(test_client, setup_login_teacher, setup_class):
    """ClassGroupList.POST should return 201."""
    payload = {"name": "TP3", "class_id": setup_class, "is_main_group": False}

    response = test_client.post("/class_groups/", json=payload)
    assert response.status_code == 201


def test_get_class_group_by_id_route(test_client, setup_class_group):
    """ClassGroupResource.GET should return 200."""
    response = test_client.get(f"/class_groups/{setup_class_group}")
    assert response.status_code == 200


def test_get_class_group_message_route(test_client):
    """ClassGroupResource.GET should return 200."""
    response = test_client.get("/class_groups/2/messages")
    assert response.status_code == 200


def test_post_class_group_message_route(test_client, setup_login_teacher):
    """ClassGroupResource.POST should return 201."""
    payload = {
        "content": "Hello World",
    }
    response = test_client.post("/class_groups/2/messages", json=payload)
    assert response.status_code == 201


def test_delete_class_group_route(test_client, setup_login_teacher, setup_class_group):
    """ClassGroupResource.DELETE should return 200."""
    response = test_client.delete(f"/class_groups/{setup_class_group}")
    assert response.status_code == 204
