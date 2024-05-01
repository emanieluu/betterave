"""Tests for the authentication endpoints."""

# type: ignore
from betterave_backend.app.models import UserLevel, UserType
from betterave_backend.app.operations import user_operations


def test_login_route(test_client):
    """LoginUser.POST should return 200 if the user is authenticated."""
    user_id = user_operations.add_user("Martine", "Garcia", "martine_garcia.jpg", UserType.STUDENT, UserLevel._1A)
    assert user_id is not None

    paylod_login = {"email": "martine.garcia@ensae.fr", "password": "mgarcia"}

    response = test_client.post("/auth/login", json=paylod_login)
    assert response.status_code == 200


def test_check_authenticated_route(test_client):
    """CheckAuthentication.GET should return 200 if the user is authenticated."""
    test_login_route(test_client)

    # Send a GET request to the check-auth endpoint
    response = test_client.get("/auth/check-auth")

    assert response.status_code == 200


def test_logout_route(test_client):
    """LogoutUser.POST should return 200 if the user is logged out."""
    test_login_route(test_client)
    response = test_client.post("/auth/logout")

    assert response.status_code == 200
