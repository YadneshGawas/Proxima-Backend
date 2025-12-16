import uuid
from datetime import datetime
from app.extensions import db

class HackathonRegistration(db.Model):
    __tablename__ = "hackathon_registrations"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))

    hackathon_id = db.Column(
        db.String,
        db.ForeignKey("hackathons.id"),
        nullable=False
    )

    user_id = db.Column(
        db.String,
        db.ForeignKey("users.id"),
        nullable=True
    )

    team_id = db.Column(
        db.String,
        db.ForeignKey("hackathon_teams.id"),
        nullable=True
    )

    status = db.Column(
        db.Enum("pending", "approved", "rejected", name="registration_status"),
        default="pending"
    )

    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationships
    hackathon = db.relationship("Hackathon", backref="registrations")
    user = db.relationship("User", backref="individual_registrations")
    team = db.relationship("HackathonTeam", backref="team_registrations")

    __table_args__ = (
        # Prevent duplicate registrations
        db.UniqueConstraint(
            "hackathon_id", "user_id", name="uq_hackathon_user_registration"
        ),
        db.UniqueConstraint(
            "hackathon_id", "team_id", name="uq_hackathon_team_registration"
        ),
    )
