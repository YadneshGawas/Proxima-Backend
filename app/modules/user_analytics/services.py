from app.extensions import db
from app.modules.registration.model import HackathonRegistration
from app.modules.winners.models import Winner
from app.modules.submissions.models import ProjectSubmission
from app.modules.teams.models import HackathonTeam, HackathonTeamMember
from app.modules.hackathons.models import Hackathon

from sqlalchemy import or_
class UserAnalyticsService:

    @staticmethod
    def get_user_analytics(user_id: int):
        # --------------------------------------------------
        # 1️⃣ Total hackathons participated
        # --------------------------------------------------
        total_hackathons = (
                db.session.query(HackathonRegistration.hackathon_id)
                .outerjoin(
                    HackathonTeam,
                    HackathonTeam.id == HackathonRegistration.team_id
                )
                .outerjoin(
                    HackathonTeamMember,
                    HackathonTeamMember.hackathon_team_id == HackathonTeam.id
                )
                .filter(
                    or_(
                        HackathonRegistration.user_id == user_id,      # individual
                        HackathonTeamMember.member_id == user_id       # team
                    )
                )
                .distinct()
                .count()
            )

        # --------------------------------------------------
        # 2️⃣ Wins (1st place)
        # --------------------------------------------------
        wins = (
            db.session.query(Winner)
            .join(ProjectSubmission, Winner.project_id == ProjectSubmission.id)
            .join(HackathonTeam, ProjectSubmission.team_id == HackathonTeam.id)
            .join(
                HackathonTeamMember,
                HackathonTeamMember.hackathon_team_id == HackathonTeam.id
            )
            .filter(HackathonTeamMember.member_id == user_id)
            .filter(Winner.position == 1)
            .count()
        )

        # --------------------------------------------------
        # 3️⃣ Runner-up (2nd & 3rd place)
        # --------------------------------------------------
        runner_up = (
            db.session.query(Winner)
            .join(ProjectSubmission, Winner.project_id == ProjectSubmission.id)
            .join(HackathonTeam, ProjectSubmission.team_id == HackathonTeam.id)
            .join(
                HackathonTeamMember,
                HackathonTeamMember.hackathon_team_id == HackathonTeam.id
            )
            .filter(HackathonTeamMember.member_id == user_id)
            .filter(Winner.position.in_([2, 3]))
            .count()
        )

        # --------------------------------------------------
        # 4️⃣ Participated but not podium
        # --------------------------------------------------
        participated = max(
            total_hackathons - (wins + runner_up),
            0
        )

        # --------------------------------------------------
        # 5️⃣ Current active team (latest joined)
        # --------------------------------------------------
        current_team = (
            db.session.query(HackathonTeam)
            .join(HackathonTeamMember)
            .filter(HackathonTeamMember.member_id == user_id)
            .order_by(HackathonTeamMember.joined_at.desc())
            .first()
        )

        current_team_data = None
        if current_team:
            current_team_data = {
                "id": current_team.id,
                "name": current_team.name,
            }

        # --------------------------------------------------
        # 6️⃣ Recent participation (last 5 hackathons)
        # --------------------------------------------------
        recent_participation = []

        recent_regs = (
            db.session.query(HackathonRegistration, Hackathon)
            .join(Hackathon, Hackathon.id == HackathonRegistration.hackathon_id)
            .outerjoin(HackathonTeam, HackathonTeam.id == HackathonRegistration.team_id)
            .outerjoin(
                HackathonTeamMember,
                HackathonTeamMember.hackathon_team_id == HackathonTeam.id
            )
            .filter(
                db.or_(
                    HackathonRegistration.user_id == user_id,              # individual
                    HackathonTeamMember.member_id == user_id               # team
                )
            )
            .order_by(HackathonRegistration.registered_at.desc())
            .limit(5)
            .all()
        )

        for reg, hackathon in recent_regs:
            winner = (
                db.session.query(Winner)
                .join(ProjectSubmission)
                .join(HackathonTeam)
                .join(HackathonTeamMember)
                .filter(HackathonTeamMember.member_id == user_id)
                .filter(ProjectSubmission.hackathon_id == hackathon.id)
                .first()
            )

            recent_participation.append({
                "hackathon_id": hackathon.id,
                "hackathon_name": hackathon.event_name,
                "team_name": reg.team.name if reg.team else "Individual",
                "position": winner.position if winner else None,
                "participated_at": reg.registered_at.isoformat()
            })

        # --------------------------------------------------
        # ✅ Final response (frontend-ready)
        # --------------------------------------------------
        return {
            "total_hackathons": total_hackathons,
            "wins": wins,
            "runner_up": runner_up,
            "participated": participated,
            "current_team": current_team_data,
            "recent_participation": recent_participation
        }
