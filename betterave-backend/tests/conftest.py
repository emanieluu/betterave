# type: ignore
# flake8: noqa
import pytest
import sys
import os

sys.path.append(os.path.join(os.getcwd(), "betterave_backend"))

from betterave_backend.create_app import create_app
from betterave_backend.extensions import db
from flask.testing import FlaskClient


class CustomClient(FlaskClient):
    """Customer client to add the API key to the request headers."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def open(self, *args, **kwargs):
        headers = kwargs.setdefault("headers", {})
        headers["X-API-KEY"] = os.environ.get("API_KEY", "BETTERAVEAPIKEY9999")
        return super().open(*args, **kwargs)


@pytest.fixture(scope="function")
def test_client():
    app = create_app(db_test_path="sqlite:///:memory:")
    app.test_client_class = CustomClient

    context = app.app_context()
    context.push()
    with app.test_client() as client:
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()
    context.pop()
