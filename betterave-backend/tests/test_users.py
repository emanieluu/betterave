"""Tests for the users endpoints."""

# type: ignore
from datetime import date
import pytest
from betterave_backend.app.models import UserType, UserLevel
from betterave_backend.app.operations.user_operations import add_user
from betterave_backend.app.operations.class_group_operations import add_class_group
from betterave_backend.app.operations.class_operations import add_class

LESSON_ID = "lesson_2"
DATE = str(date(2023, 12, 21))
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
def setup_student(test_client) -> int:
    """Create a user and returns their ID."""
    student_id = add_user("Alice", "Georges", "student_pic_url", UserType.STUDENT, UserLevel._3A)
    return student_id


@pytest.fixture
def setup_teacher(test_client) -> int:
    """Create a user and returns their ID."""
    teacher_id = add_user("John", "Martins", "teacher_pic_url", UserType.TEACHER, UserLevel.NA)
    return teacher_id


@pytest.fixture
def setup_association(test_client) -> int:
    """Create an asso user and returns their ID."""
    asso_id = add_user("BDS", "", "asso_pic_url", UserType.ASSO, UserLevel.NA)
    return asso_id


@pytest.fixture
def setup_login_admin(test_client, setup_admin) -> int:
    """Login admin."""
    paylod_login = {"email": "directeur.admin@ensae.fr", "password": "dadmin"}

    response_login = test_client.post("/auth/login", json=paylod_login)
    return response_login


@pytest.fixture
def setup_login_student(test_client, setup_student) -> int:
    """Login student."""
    paylod_login = {"email": "alice.georges@ensae.fr", "password": "ageorges"}
    response_login = test_client.post("/auth/login", json=paylod_login)
    return response_login


@pytest.fixture
def setup_class(test_client, setup_teacher) -> int:
    """Fixture to create a class and return its instance."""
    class_id = add_class(
        class_id=1,
        name="Betterave",
        ects_credits=20,
        default_teacher_id=setup_teacher,
        level="3A",
        background_color="#123456",
    )
    return class_id


@pytest.fixture
def setup_group(test_client, setup_class) -> int:
    """Create a group and return its instance."""
    group_id = add_class_group(
        name="Test Group",
        is_main_group=True,
        class_id=setup_class,
    )
    return group_id


def test_get_all_users_route(test_client):
    """UserList.GET should return 200."""
    response = test_client.get("/users/")
    assert response.status_code == 200


def test_post_user_route(test_client, setup_login_admin):
    """UserList.POST should return 201."""
    payload = {
        "name": "Alice",
        "surname": "Dupont",
        "profile_pic": "photos/alice_dupont.jpg",
        "email_override": None,
        "profile_pic": "photos/alice_dupont.jpg",
        "level": "3A",
        "user_type": "student",
        "password_override": None,
    }
    response = test_client.post("/users/", json=payload)
    assert response.status_code == 201


def test_get_students_route(test_client, setup_class, setup_group):
    """ClassListStudents.GET should return 200."""
    response = test_client.get(f"/users/studentlist/{setup_class}")
    assert response.status_code == 200


def test_post_student_route(test_client, setup_class, setup_login_admin):
    """ClassListStudents.POST should return 201."""
    payload = {
        "name": "Alice",
        "surname": "Dupont",
        "profile_pic": "photos/alice_dupont.jpg",
        "email_override": None,
        "level": "3A",
        "user_type": "student",
        "password_override": None,
    }
    response = test_client.post(f"/users/studentlist/{setup_class}", json=payload)
    assert response.status_code == 201


def test_get_grades_route(test_client, setup_class, setup_student):
    """GradesByStudentAndClass.GET should return 200."""
    response = test_client.get(f"/users/{setup_class}/grades/{setup_student}")
    assert response.status_code == 200


def put_grades_route(test_client, setup_login_admin, setup_class, setup_student):
    """GradesByStudentAndClass.PUT should return 200."""
    payload = {"grade": 15}
    response = test_client.put(f"/users/{setup_class}/grades/{setup_student}", json=payload)
    assert response.status_code == 200


def test_get_user_by_id_route(test_client, setup_student):
    """UserRessource.GET should return 200."""
    response = test_client.get(f"/users/{setup_student}")
    assert response.status_code == 200


def test_update_user_by_id_route(test_client, setup_student, setup_login_admin):
    """UserRessource.PUT should return 200."""
    payload = {
        "level": "2A",
    }
    response = test_client.put(f"/users/{setup_student}", json=payload)
    assert response.status_code == 204


def test_get_user_lessons_route(test_client, setup_student, setup_login_student):
    """UserLessons.GET should return 200."""
    response = test_client.get(f"/users/{setup_student}/lessons")
    assert response.status_code == 200


def test_get_user_future_lessons_route(test_client, setup_student, setup_login_student):
    """UserFutureLessons.GET should return 200."""
    response = test_client.get(f"/users/{setup_student}/lessons/future")
    assert response.status_code == 200


def test_get_all_associations_route(test_client, setup_student, setup_association):
    """AssociationList.GET should return 200."""
    response = test_client.get("/users/associations")
    assert response.status_code == 200


def test_get_user_association_route(test_client, setup_student, setup_login_student):
    """UserAssociationList.GET should return 200."""
    response = test_client.get(f"/users/associations/{setup_student}")
    assert response.status_code == 200


def test_post_user_association_route(test_client, setup_student, setup_association, setup_login_student):
    """SubscribeAssociation.POST should return 201."""
    response = test_client.post(f"/users/{setup_student}/subscribe/{setup_association}")
    assert response.status_code == 200


def test_unsubscribe_user_association_route(test_client, setup_student, setup_association, setup_login_student):
    """UnsubscribeAssociation.DELETE should return 200."""
    test_post_user_association_route(test_client, setup_student, setup_association, setup_login_student)
    response = test_client.delete(f"/users/{setup_student}/unsubscribe/{setup_association}")
    assert response.status_code == 200


def test_get_user_events_route(test_client, setup_student, setup_login_student):
    """UserEvents.GET should return 200."""
    response = test_client.get(f"/users/{setup_student}/events")
    assert response.status_code == 200


def test_get_user_future_events_route(test_client, setup_student, setup_login_student):
    """UserFutureEvents.GET should return 200."""
    response = test_client.get(f"/users/{setup_student}/events/future")
    assert response.status_code == 200


def test_delete_user_by_id_route(test_client, setup_student, setup_login_admin):
    """UserRessource.DELETE should return 200."""
    response = test_client.delete(f"/users/{setup_student}")
    assert response.status_code == 204
