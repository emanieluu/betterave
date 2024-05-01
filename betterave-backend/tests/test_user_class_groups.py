"""Tests for the user class groups endpoints ."""

# type: ignore
import pytest
from betterave_backend.app.models import UserType, UserLevel
from betterave_backend.app.operations.user_operations import add_user
from betterave_backend.app.operations.class_group_operations import add_class_group
from betterave_backend.app.operations.class_operations import add_class
from betterave_backend.app.operations.user_class_group_operations import add_user_class_group


@pytest.fixture
def setup_admin(test_client) -> int:
    """Create a user and returns their ID."""
    admin_id = add_user("Directeur", "Admin", "teacher_pic_url", UserType.ADMIN, UserLevel.NA)
    return admin_id


@pytest.fixture
def setup_student(test_client) -> int:
    """Create a user and returns their ID."""
    student_id = add_user("Alice", "Georges", "student_pic_url", UserType.STUDENT, UserLevel._1A)
    return student_id


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
def setup_primary_class_group(test_client, setup_class) -> int:
    """Create a group and return its instance."""
    group_id = add_class_group(
        name="Test Group",
        is_main_group=True,
        class_id=setup_class,
    )
    return group_id


@pytest.fixture
def setup_secondary_class_group(test_client, setup_class) -> int:
    """Create a group and return its instance."""
    group_id = add_class_group(
        name="Test Group 2",
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
def setup_user_class_group(
    test_client, setup_student, setup_class, setup_primary_class_group, setup_secondary_class_group
) -> int:
    """Create a user class group."""
    user_class_group_id = add_user_class_group(
        user_id=setup_student,
        class_id=setup_class,
        primary_class_group_id=setup_primary_class_group,
        secondary_class_group_id=setup_secondary_class_group,
    )
    return user_class_group_id


def test_post_user_class_group_route(
    test_client, setup_login_admin, setup_student, setup_class, setup_primary_class_group
):
    """UserClassGroupList.POST should return 201."""
    payload = {
        "user_id": setup_student,
        "class_id": setup_class,
        "primary_class_group_id": setup_primary_class_group,
        "secondary_class_group_id": None,
    }
    response = test_client.post("/user_class_groups/", json=payload)
    assert response.status_code == 201


def test_get_user_class_group_by_id_route(test_client, setup_user_class_group):
    """UserClassGroupResource.GET should return 200."""
    response = test_client.get(f"/user_class_groups/{setup_user_class_group}")
    assert response.status_code == 200


def test_delete_user_class_group_route(test_client, setup_user_class_group):
    """UserClassGroupResource.DELETE should return 204."""
    response = test_client.delete(f"/user_class_groups/{setup_user_class_group}")
    assert response.status_code == 204
