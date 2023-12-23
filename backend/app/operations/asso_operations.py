from extensions import db
from app.decorators import with_instance
from app.models.user import User, UserType
from sqlalchemy.exc import SQLAlchemyError
from app.operations.event_operations import get_association_future_events
from app.operations.notification_operations import get_association_notifications

@with_instance([User, User])
def subscribe_to_asso(user: User, asso: User) -> bool:
    """Subscribe a user to an association."""
    try:
        # If already subscribed, no need to proceed
        if asso in user.subscriptions:
            return True

        user.subscriptions.append(asso)

        future_events = get_association_future_events(asso)
        #notifications = get_association_notifications(asso)
        
        #for notif in notifications:
            #notif.recipient_users.append(user)
        
        for event in future_events:
            event.attending_users.append(user)

        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error subscribing user to asso: {str(e)}")
        return False


@with_instance([User, User])
def unsubscribe_from_asso(user: User, asso: User) -> bool:
    """Unsubscribe a user from an association."""
    try:
        # If not subscribed, no need to proceed
        if asso not in user.subscriptions:
            return True

        user.subscriptions.remove(asso)

        future_events = get_association_future_events(asso)
        notifications = get_association_notifications(asso)
        
        for notif in notifications:
            if user in notif.recipient_users:
                notif.recipient_users.remove(user)
            
        for event in future_events:
            if user in event.attending_users:
                event.attending_users.remove(user)

        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error unsubscribing user from asso: {str(e)}")
        return False


def get_all_assos():
    """Get all associations."""
    return User.query.filter_by(user_type=UserType("asso")).all()
