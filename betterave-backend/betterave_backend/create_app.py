"""App factory module."""

import os
import subprocess
import json

from typing import Optional
from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from betterave_backend.extensions import db, bcrypt, login_manager, api, mail

from betterave_backend.app.api import (
    auth_ns,
    users_ns,
    classes_ns,
    lessons_ns,
    class_groups_ns,
    user_class_groups_ns,
    events_ns,
    notifications_ns,
)


@login_manager.user_loader
def load_user(user_id: int):  # type: ignore
    """Load the user from the database."""
    from betterave_backend.app.models.user import User

    return User.query.get(int(user_id))


def detect_ssp_cloud():
    """Check if the app is running on SSP Cloud."""
    return "/home/onyxia" in os.getenv("WORKSPACE_DIR", "")


def create_app(db_test_path: Optional[str] = None) -> Flask:
    """Create the application instance."""
    print(f"Creating app from {os.getcwd()}", flush=True)
    print("API KEY:", os.environ.get("API_KEY"))

    # Initialize the Flask app
    app = Flask(__name__)
    app.config["TESTING"] = db_test_path is not None
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or b"\x05\xe1C\x07k\x1ay<\xb6\xa4\xf8\xc6\xa8f\xb4*"

    if detect_ssp_cloud():
        print("Working on SSP Cloud...")
        # Use the Vault secrets
        VAULT_PATH = os.getenv("VAULT_RELATIVE_PATH")
        result = subprocess.run(["vault", "kv", "get", "-format=json", VAULT_PATH], capture_output=True, text=True)
        if result.returncode == 0:
            secret_data = json.loads(result.stdout)["data"]["data"]
        else:
            print(f"Error fetching secret: {result.stderr}")

        POSTGRES_PORT = secret_data["POSTGRES_PORT"]
        POSTGRES_USER = secret_data["POSTGRES_USER"]
        POSTGRES_PW = secret_data["POSTGRES_PW"]
        POSTGRES_HOSTNAME = secret_data["POSTGRES_HOSTNAME"]
        POSTGRES_DB = secret_data["POSTGRES_DB"]
        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = f"postgresql://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{POSTGRES_DB}"

    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = db_test_path if db_test_path else "sqlite:////database/betterave.db"

    app.config.update(
        DEBUG=True,
        SESSION_COOKIE_HTTPONLY=True,
        REMEMBER_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Strict",
    )
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

    CORS(
        app,
        supports_credentials=True,
        resources={
            r"/*": {
                "origins": [
                    "http://localhost:8080",
                    "http://127.0.0.1:8080",
                    "https://betterave.kientz.net",
                    "http://89.168.39.28:8080" "https://89.168.39.28:8080",
                ],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": [
                    "Content-Type",
                    "Authorization",
                    "X-Requested-With",
                    "Accept",
                ],
                "expose_headers": [
                    "Access-Control-Allow-Origin",
                    "Access-Control-Allow-Credentials",
                ],
            }
        },
    )

    # Initialize Flask-Mail
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = "sbetterave.mdp@gmail.com"
    app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
    print(f"MAIL_PASSWORD: {os.environ.get('MAIL_PASSWORD')}")
    mail.init_app(app)  # Bind Flask-Mail to the Flask application

    # Initialize the extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    api.init_app(app)

    # Initialize the Flask-RestX Api and register the namespaces
    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(users_ns, path="/users")
    api.add_namespace(classes_ns, path="/classes")
    api.add_namespace(lessons_ns, path="/lessons")
    api.add_namespace(class_groups_ns, path="/class_groups")
    api.add_namespace(user_class_groups_ns, path="/user_class_groups")
    api.add_namespace(events_ns, path="/events")
    api.add_namespace(notifications_ns, path="/notifications")

    # Load/create the database
    with app.app_context():
        db.create_all()
        db.session.commit()

    # For testing purposes
    @app.route("/hello")
    def index() -> str:
        """Route for testing purposes."""
        return "Hello, World!"

    return app
