from datetime import datetime
from app.extensions import db

from app.modules.hackathons.models import Hackathon
from app.modules.registration.model import HackathonRegistration
from app.modules.teams.models import HackathonTeam

from app.modules.registration.exceptions import (
    HackathonNotFoundError,
    RegistrationClosedError,
    InvalidParticipationTypeError,
    DuplicateRegistrationError,
    TeamRequiredError,
    TeamNotFoundError,
    TeamMembershipError,
    TeamSizeError,
    RegistrationNotFoundError,
)


class RegistrationService:

    @staticmethod
    def register(hackathon_id, user_id, team_id=None):
        hackathon = Hackathon.query.get(hackathon_id)
        if not hackathon:
            raise HackathonNotFoundError("Hackathon not found")

        # Deadline enforcement
        if hackathon.deadline and hackathon.deadline < datetime.utcnow():
            raise RegistrationClosedError("Registration deadline has passed")

        # ───────────── Individual Registration ─────────────
        if hackathon.participation_type == "individual":
            if team_id:
                raise InvalidParticipationTypeError(
                    "This hackathon allows individual participation only"
                )

            existing = HackathonRegistration.query.filter_by(
                hackathon_id=hackathon_id,
                user_id=user_id
            ).first()

            if existing:
                raise DuplicateRegistrationError("User already registered")

            registration = HackathonRegistration(
                hackathon_id=hackathon_id,
                user_id=user_id
            )

        # ───────────── Team Registration ─────────────
        elif hackathon.participation_type == "team":
            if not team_id:
                raise TeamRequiredError("Team registration required")

            team = HackathonTeam.query.get(team_id)
            if not team:
                raise TeamNotFoundError("Team not found")

            member_ids = [member.member_id for member in team.members]

            if int(user_id) not in member_ids:
                raise TeamMembershipError(
                    "User is not a member of this team"
                )

            team_size = len(team.members)

            if hackathon.min_team_size and team_size < hackathon.min_team_size:
                raise TeamSizeError("Team size is below minimum requirement")

            if hackathon.max_team_size and team_size > hackathon.max_team_size:
                raise TeamSizeError("Team size exceeds maximum limit")

            existing = HackathonRegistration.query.filter_by(
                hackathon_id=hackathon_id,
                team_id=team_id
            ).first()

            if existing:
                raise DuplicateRegistrationError("Team already registered")

            registration = HackathonRegistration(
                hackathon_id=hackathon_id,
                team_id=team_id
            )

        else:
            raise InvalidParticipationTypeError("Invalid participation type")

        db.session.add(registration)
        db.session.commit()
        return registration

    # ───────────── Status Update ─────────────
    @staticmethod
    def update_status(registration_id, status):
        registration = HackathonRegistration.query.get(registration_id)
        if not registration:
            raise RegistrationNotFoundError("Registration not found")

        registration.status = status
        db.session.commit()
        return registration

    # ───────────── Query Methods ─────────────
    @staticmethod
    def get_user_registrations(user_id):
        return HackathonRegistration.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_team_registrations(team_id):
        return HackathonRegistration.query.filter_by(team_id=team_id).all()

    @staticmethod
    def get_hackathon_registrations(hackathon_id):
        return HackathonRegistration.query.filter_by(
            hackathon_id=hackathon_id
        ).all()
