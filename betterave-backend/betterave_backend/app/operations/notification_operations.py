# type: ignore
from typing import Optional
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from betterave_backend.extensions import db
from betterave_backend.app.models import Notification, User, UserLevel
from betterave_backend.app.decorators import is_valid_apikey, with_instance


def add_notification(
    title: str,
    content: str,
    sent_by_user_id: int,
    recipient_type: [str, UserLevel],
) -> int:
    """Add a notification to the database."""
    try:
        if recipient_type == "Subscribers":
            recipient_users = User.query.get(sent_by_user_id).subscribers
        elif recipient_type == "All users":
            recipient_users = User.query.all()
        elif isinstance(recipient_type, UserLevel):
            recipient_users = User.query.filter_by(level=recipient_type).all()
        else:
            raise ValueError("Invalid recipient_type")

        new_notification = Notification(
            title=title,
            content=content,
            sent_by_user_id=sent_by_user_id,
            recipient_type=recipient_type,
            recipient_users=recipient_users,
        )

        db.session.add(new_notification)
        db.session.commit()

        return new_notification.notification_id
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error adding notification: {str(e)}")
        return -1


def update_notification(notification_id: int, new_data: dict) -> bool:
    """Modify notification information in the database."""
    try:
        notification = get_notification_by_id(notification_id)
        if notification:
            for key, value in new_data.items():
                if hasattr(notification, key):
                    setattr(notification, key, value)
            db.session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error modifying notification: {str(e)}")
        return False


def delete_notification(notification_id: int) -> bool:
    """Remove a notification from the database."""
    try:
        notification = get_notification_by_id(notification_id)
        if notification:
            db.session.delete(notification)
            db.session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error deleting notification: {str(e)}")
        return False


def get_notification_by_id(notification_id: int) -> Notification:
    """Get a notification by its ID."""
    return db.session.get(Notification, notification_id)


def get_all_notifications() -> list[Notification]:
    """Return all notifications in the database."""
    return Notification.query.all()


def get_title_notification_by_id(notification_id: int) -> Notification:
    """Get a notification by its ID."""
    notif = db.session.get(Notification, notification_id)
    return notif.title


@with_instance(User)
def get_user_notifications(user: User, limit: Optional[int] = None) -> list[Notification]:
    """Get all events a particular user is attending."""
    if limit is not None:
        notification = user.received_notifications[:limit]
    else:
        notification = user.received_notifications

    return notification


def add_recipient_to_notification(notification_id: int, user_ids=None, user_level=None):
    """Link new recipients to a notification. If no users are specified, link all users."""
    notification = Notification.query.get(notification_id)
    if not notification:
        return False

    if user_ids:
        # Link specific users (recipients) to the notification
        users = User.query.filter(User.user_id.in_(user_ids)).all()
        notification.recipient_users.extend(users)

    elif user_level:
        # Link all users of a certain level to the notification
        users = User.query.filter_by(level=user_level).all()
        notification.recipient_users.extend(users)
    else:
        # If no specific users or level provided, assume linking all users
        users = User.query.all()
        notification.recipient_users.extend(users)

    db.session.commit()
    return True


def can_create_notification(user: User) -> bool:
    """Check if a user can create a notification."""
    # Assume that admin can create notifications for him, for any association or for all users
    apikey = request.headers.get("X-API-KEY")
    if apikey and is_valid_apikey(apikey):
        return True
    if user.is_admin:
        return True
    # Associations can only create notifications for themselves
    if user.is_asso:
        return True
    return False
