"""Flask SQLAlchemy model for a notification."""

from betterave_backend.extensions import db


class Notification(db.Model):
    """SQLAlchemy object representing a notification."""

    __tablename__ = "notification"
    notification_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    sent_by_user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    recipient_type = db.Column(db.String, nullable=False)

    # Relationships
    recipient_users = db.relationship(
        "User",
        secondary="notification_reception",
        back_populates="received_notifications",
    )
    sender = db.relationship("User", foreign_keys=[sent_by_user_id])
