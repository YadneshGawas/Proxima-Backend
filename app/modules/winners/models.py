# app/modules/winners/models.py
import uuid
from datetime import datetime
from app.extensions import db


class Winner(db.Model):
    __tablename__ = "winners"

    id = db.Column(
        db.String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    project_id = db.Column(
        db.String,
        db.ForeignKey("project_submissions.id"),
        nullable=False
    )

    position = db.Column(db.Integer, nullable=False)  # 1,2,3

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships (used only when querying)
    project = db.relationship("ProjectSubmission", lazy="joined")

    __table_args__ = (
        db.UniqueConstraint(
            "project_id",
            name="uq_project_winner"
        ),
        db.UniqueConstraint(
            "position",
            "project_id",
            name="uq_position_project"
        ),
    )
