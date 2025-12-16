from app.extensions import db
from datetime import datetime,timezone
from enum import Enum
import uuid


class TeamMemberRole(Enum):
    OWNER = "owner"
    COLEADER = "coleader"           
    MEMBER = "member"

class HackathonTeam(db.Model):
    __tablename__ = "hackathon_teams"
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(150),nullable=False)
    created_by = db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
     # ✅ EXPLICIT relationship
    members = db.relationship(
        "HackathonTeamMember",
        back_populates="team",
        cascade="all, delete-orphan",
        lazy="joined"
    )


class HackathonTeamMember(db.Model):
    __tablename__ = 'hackathon_team_members'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    hackathon_team_id = db.Column(db.String,db.ForeignKey("hackathon_teams.id"),nullable=False)
    member_id = db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    role = db.Column(db.Enum(TeamMemberRole, name="team_member_role"),default=TeamMemberRole.MEMBER)
    joined_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

     # ✅ MATCHES back_populates
    team = db.relationship("HackathonTeam", back_populates="members")

    # ✅ User relationship (for name, email, etc.)
    user = db.relationship("User", lazy="joined")