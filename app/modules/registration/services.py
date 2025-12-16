from datetime import datetime
from app.extensions import db

from app.modules.hackathons.models import Hackathon
from app.modules.registration.model import HackathonRegistration
from app.modules.teams.models import HackathonTeam
from app.modules.registration.schemas import RegistrationResponseSchema
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
        registrations = HackathonRegistration.query.filter_by(
            hackathon_id=hackathon_id
        ).all()

        result = []

        for reg in registrations:
            data = {
                "id": reg.id,
                "hackathon_id": reg.hackathon_id,
                "user_id": reg.user_id,
                "team_id": reg.team_id,
                "status": reg.status,
                "registered_at": reg.registered_at,
                "team": None
            }

            # Team-based registration
            if reg.team_id:
                team = HackathonTeam.query.get(reg.team_id)
                if team:
                    data["team"] = {
                        "id": team.id,
                        "name": team.name,
                        "created_by": team.created_by,
                        "members": [
                            {
                                "user_id": m.member_id,
                                "name": m.user.name, 
                                "role": m.role.value,
                                "joined_at": m.joined_at
                            }
                            for m in team.members
                        ]
                    }

            result.append(data)

        return result

    @staticmethod
    def check_user_registration(hackathon_id, user_id):
        user_id = int(user_id)

        # Ensure hackathon exists (avoid silent false)
        hackathon = Hackathon.query.get(hackathon_id)
        if not hackathon:
            raise HackathonNotFoundError("Hackathon not found")

        # 1️⃣ Check individual registration
        individual = HackathonRegistration.query.filter_by(
            hackathon_id=hackathon_id,
            user_id=user_id
        ).first()

        if individual:
            return {
                "registered": True,
                "status": individual.status,
                "mode": "individual",
                "registration_id": individual.id,
                "team_id": None
            }

        # 2️⃣ Check team-based registration
        team_regs = (
            HackathonRegistration.query
            .filter_by(hackathon_id=hackathon_id)
            .filter(HackathonRegistration.team_id.isnot(None))
            .all()
        )

        for reg in team_regs:
            team = HackathonTeam.query.get(reg.team_id)
            if not team:
                continue

            member_ids = {m.member_id for m in team.members}
            if user_id in member_ids:
                return {
                    "registered": True,
                    "status": reg.status,
                    "mode": "team",
                    "registration_id": reg.id,
                    "team_id": reg.team_id
                }

        # 3️⃣ Not registered
        return {
            "registered": False
        }

    @staticmethod
    def get_hackathon_analytics(hackathon_id):
        hackathon = Hackathon.query.get(hackathon_id)
        if not hackathon:
            raise HackathonNotFoundError("Hackathon not found")

        # Base query
        registrations = HackathonRegistration.query.filter_by(
            hackathon_id=hackathon_id
        ).all()

        total_registrations = len(registrations)

        approved = sum(1 for r in registrations if r.status == "approved")
        pending = sum(1 for r in registrations if r.status == "pending")
        rejected = sum(1 for r in registrations if r.status == "rejected")

        total_participants = 0

        for reg in registrations:
            # Individual registration
            if reg.user_id:
                total_participants += 1

            # Team registration
            elif reg.team_id:
                team = HackathonTeam.query.get(reg.team_id)
                if team:
                    total_participants += len(team.members)

        return {
            "total_registrations": total_registrations,
            "approved": approved,
            "pending": pending,
            "rejected": rejected,
            "total_participants": total_participants
        }