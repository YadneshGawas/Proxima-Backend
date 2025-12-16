import uuid
from datetime import datetime
from app.extensions import db


class ProjectSubmission(db.Model):
    __tablename__ = "project_submissions"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))

    hackathon_id = db.Column(
        db.String,
        db.ForeignKey("hackathons.id"),
        nullable=False
    )

    team_id = db.Column(
        db.String,
        db.ForeignKey("hackathon_teams.id"),
        nullable=False
    )

    project_title = db.Column(db.String(255), nullable=False)
    project_desc = db.Column(db.Text, nullable=False)
    github_url = db.Column(db.String(500), nullable=False)
    live_url = db.Column(db.String(500), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    hackathon = db.relationship("Hackathon", backref="project_submissions")
    team = db.relationship("HackathonTeam", backref="project_submissions")
    scores = db.relationship(
        "JudgeScore",
        backref="submission",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "hackathon_id",
            "team_id",
            name="uq_hackathon_team_submission"
        ),
    )


class JudgeScore(db.Model):
    __tablename__ = "judge_scores"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))

    submission_id = db.Column(
        db.String,
        db.ForeignKey("project_submissions.id"),
        nullable=False
    )

    judge_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint(
            "submission_id",
            "judge_id",
            name="uq_submission_judge_score"
        ),
    )


class HackathonJudge(db.Model):
    __tablename__ = "hackathon_judges"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    hackathon_id = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint(
            "hackathon_id",
            "user_id",
            name="uq_hackathon_judge"
        ),
    )
