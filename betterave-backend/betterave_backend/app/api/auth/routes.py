# type: ignore
from flask import request
from flask_restx import Resource
from flask_login import login_user, current_user, logout_user
from flask_mail import Message
from .namespace import api
from .models import login_model, login_status_model, reset_password_model
from betterave_backend.app.operations.user_operations import (
    check_password,
    get_user_by_email,
    set_new_token,
    update_user_password,
)
from betterave_backend.extensions import mail
import secrets


@api.route("/login")
class LoginUser(Resource):
    @api.expect(login_model)
    def post(self):
        """Try to login user."""
        if current_user.is_authenticated:
            return {"message": "User already logged in"}, 200
        data = api.payload
        email = data["email"]
        password = data["password"]
        user = get_user_by_email(email)

        if user and check_password(user.hashed_password, password):
            login_user(user)
            message = user.user_type.value.capitalize() + " login successful"
            return {"message": message}, 200
        api.abort(401, "Invalid email or password")


@api.route("/logout")
class LogoutUser(Resource):
    def post(self):
        """Logout user."""
        logout_user()
        return {"message": "Logged out successfully", "status": "success"}, 200


@api.route("/check-auth")
class CheckAuthentication(Resource):
    @api.marshal_with(login_status_model)
    def get(self):
        """Check if user is authenticated."""
        if current_user.is_authenticated:
            return {
                "status": "authenticated",
                "role": current_user.user_type.value,
            }, 200
        api.abort(401, "User not authenticated")


@api.route("/reset-password")
class ResetPassword(Resource):
    @api.expect(reset_password_model)
    def post(self):
        """Reset user's password and send reset instructions via email."""
        data = api.payload
        email = data["email"]
        user = get_user_by_email(email)
        if user:
            # Generate a secure reset token
            reset_token = secrets.token_urlsafe(20)
            set_new_token(user, reset_token)
            # Send password reset email
            send_password_reset_email(user)
            return {"message": "Password reset instructions sent to your email"}, 200
        else:
            api.abort(404, "User with provided email not found")


def send_password_reset_email(user):
    """Send password reset instructions to the user's email address."""
    try:
        token = user.reset_token
        email = user.email
        msg = Message(
            "Password Reset Instructions",
            sender="sbetterave.mdp@gmail.com",
            recipients=[email],
        )
        msg.body = (
            "Hello,\n\nHere is your reset token: "
            f"{token}\n\nIf you did not request this reset, "
            "please ignore this email.\n\nThank you."
        )
        mail.send(msg)
        print("Password reset email sent successfully.")
    except Exception as e:
        print(f"Error sending password reset email: {str(e)}")
        raise e


@api.route("/validate-token")
class ValidateResetToken(Resource):
    def post(self):
        """Validate the reset token."""
        data = request.get_json()
        email = data.get("email")
        reset_token = data.get("resetToken")

        user = get_user_by_email(email)
        if user and user.reset_token == reset_token:
            return {"isValid": True}, 200
        else:
            return {"isValid": False}, 400


@api.route("/reset-password-confirm")
class ResetPasswordConfirm(Resource):
    def post(self):
        """Confirm password reset with the new password."""
        data = request.get_json()
        email = data.get("email")
        new_password = data.get("newPassword")

        # Update user's password
        update_user_password(email, new_password)

        return {"message": "Password reset successful"}, 200
