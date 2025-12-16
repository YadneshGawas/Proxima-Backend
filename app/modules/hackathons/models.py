import uuid
from datetime import datetime
from app.extensions import db
from sqlalchemy import JSON

class Hackathon(db.Model):
    __tablename__ = "hackathons"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))

    organizer_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)

    event_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(255), nullable=True)

    mode = db.Column(db.Enum("online", "offline", "hybrid", name="event_mode"), nullable=False)
    participation_type = db.Column(db.Enum("individual", "team", name="participation_type"), nullable=False)

    min_team_size = db.Column(db.Integer, nullable=True)
    max_team_size = db.Column(db.Integer, nullable=True)

    deadline = db.Column(db.DateTime, nullable=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)

    entry_fee = db.Column(db.Float, default=0)
    max_participants = db.Column(db.Integer, nullable=True)

    tags = db.Column(JSON, default=list)

    interested_count = db.Column(db.Integer, default=0)
    status = db.Column(db.Enum("upcoming", "ongoing", "completed", name="hackathon_status"), default="upcoming")

    image_url = db.Column(db.String(500), nullable=True)

    requirements = db.Column(JSON, default=list)
    prizes = db.Column(JSON, default=list)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    organizer = db.relationship("User", backref="hackathons")

class HackathonInterest(db.Model):
    __tablename__ = "hackathon_interests"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    hackathon_id = db.Column(
        db.String,
        db.ForeignKey("hackathons.id"),
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("user_id", "hackathon_id", name="uq_user_hackathon"),
    )

