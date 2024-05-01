"""Tests for the class endpoints."""

# type: ignore
import pytest
from betterave_backend.app.operations.homework_operations import add_homework_to_class
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
DUE_DATE = "2023-12-31"
DUE_TIME = "23:59"
HOMEWORK_CONTENT = "Complete assignment 3"


@pytest.fixture
def setup_teacher(test_client) -> int:
    """Create a user and returns their ID."""
    teacher_id = add_user("John", "Martins", "teacher_pic_url", UserType.TEACHER, UserLevel.NA)
    return teacher_id


@pytest.fixture
def setup_admin(test_client) -> int:
    """Create a user and returns their ID."""
    admin_id = add_user("Directeur", "Admin", "teacher_pic_url", UserType.ADMIN, UserLevel.NA)
    return admin_id


@pytest.fixture
def setup_login_teacher(test_client, setup_teacher) -> int:
    """Login teacher."""
    paylod_login = {"email": "john.martins@ensae.fr", "password": "jmartins"}

    response_login = test_client.post("/auth/login", json=paylod_login)
    return response_login


@pytest.fixture
def setup_login_admin(test_client, setup_admin) -> int:
    """Login admin."""
    paylod_login = {"email": "directeur.admin@ensae.fr", "password": "dadmin"}

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
    group_id = add_class_group(name="TP 8", class_id=setup_class, is_main_group=True)
    return group_id


@pytest.fixture
def setup_homework(test_client, setup_class) -> int:
    """Fixture to create a homework and return its ID."""
    homework_id = add_homework_to_class(HOMEWORK_CONTENT, setup_class, DUE_DATE, DUE_TIME)
    return homework_id


def test_get_class_route(test_client):
    """ClassList.GET should return 200 ."""
    response = test_client.get("/classes/")
    assert response.status_code == 200
    assert response.content_type == "application/json"


def test_post_class_route(test_client, setup_login_admin, setup_teacher):
    """ClassList.POST should return 201 if the class is creaded."""
    paylod_post = {
        "class_id": 2,
        "name": "Création de Betterave",
        "ects_credits": 100,
        "ensae_link": "https://www.ensae.fr/courses/130",
        "level": "3A",
        "background_color": "#FFC071",
        "default_teacher_id": setup_teacher,
    }
    response = test_client.post("/classes/", json=paylod_post)
    assert response.status_code == 201
    assert response.content_type == "application/json"


def test_get_class_by_id_route(test_client, setup_class):
    """ClassResource.GET should return 200 if the class is found."""
    response = test_client.get(f"/classes/{setup_class}")
    assert response.status_code == 200
    assert response.content_type == "application/json"


def test_update_class_route(test_client, setup_login_admin, setup_class):
    """ClassResource.PUT should return 204 if the class is updated."""
    paylod_put = {
        "name": "Théorie des jeux Semestre 2",
    }
    response = test_client.put(f"/classes/{setup_class}", json=paylod_put)
    assert response.status_code == 204


def test_get_class_by_level_route(test_client, setup_class):
    """ClassLevelResource.GET should return 200 if the level is found."""
    response = test_client.get(f"/classes/level/{LEVEL}")
    assert response.status_code == 200
    assert response.content_type == "application/json"


def test_get_class_by_level_not_found_route(test_client):
    """ClassLevelResource.GET should return 404 if the level is not found."""
    response = test_client.get("/classes/level/3B")
    assert response.status_code == 404
    assert response.content_type == "application/json"


def test_get_teacher_classes_route(test_client, setup_teacher):
    """TeacherClasses.GET should return 200 if the teacher classes are found."""
    response = test_client.get(f"/classes/teacherclasses/{setup_teacher}")
    assert response.status_code == 200
    assert response.content_type == "application/json"


def test_post_class_message_route(test_client, setup_login_teacher, setup_class, setup_class_group):
    """ClassMessages.POST should return 201 if the message is posted."""
    paylod_post = {"content": "Bienvenue dans le cours de Théorie des jeux Semestre 2"}
    response = test_client.post(f"/classes/{setup_class}/messages", json=paylod_post)
    assert response.status_code == 201
    assert response.content_type == "application/json"


def test_get_class_homeworks_route(test_client, setup_class, setup_class_group, setup_homework):
    """ClassHomeworks.GET should return 200 if the class homeworks are found."""
    response = test_client.get(f"/classes/{setup_class}/homework")
    assert response.status_code == 200
    assert response.content_type == "application/json"


def test_post_class_homework_route(test_client, setup_login_teacher, setup_class, setup_class_group):
    """ClassHomeworks.POST should return 201 if the homework is posted."""
    paylod_post = {"content": "Faire les exercices 1, 2.", "due_date": "2024-06-26", "due_time": "00:00"}
    response = test_client.post(f"/classes/{setup_class}/homework", json=paylod_post)
    assert response.status_code == 201
    assert response.content_type == "application/json"


def test_delete_class_route(test_client, setup_login_admin, setup_class):
    """ClassResource.DELETE should return 204 if the class is deleted."""
    response = test_client.delete(f"/classes/{setup_class}")
    assert response.status_code == 204
