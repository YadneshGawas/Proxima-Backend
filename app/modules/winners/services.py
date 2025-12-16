# app/modules/winners/services.py
from werkzeug.exceptions import BadRequest
from app.extensions import db
from app.modules.winners.models import Winner
from app.modules.submissions.models import ProjectSubmission
from app.modules.submissions.services import ScoringService


class WinnerService:

    @staticmethod
    def finalize_winners(hackathon):
        # if hackathon.is_finalized:
        #     raise BadRequest("Hackathon already finalized")

        submissions = ProjectSubmission.query.filter_by(
            hackathon_id=hackathon.id
        ).all()

        if not submissions:
            raise BadRequest("No submissions to finalize")

        ranked = sorted(
            submissions,
            key=lambda s: ScoringService.calculate_average(s) or 0,
            reverse=True
        )

        winners = []

        for position, submission in enumerate(ranked[:3], start=1):
            avg = ScoringService.calculate_average(submission)
            if avg is None:
                continue

            winner = Winner(
                project_id=submission.id,
                position=position
            )

            db.session.add(winner)
            winners.append(winner)

        hackathon.is_finalized = True
        db.session.commit()

        return winners

    @staticmethod
    def list_winners(hackathon_id):
        winners = (
            Winner.query
            .join(ProjectSubmission)
            .filter(ProjectSubmission.hackathon_id == hackathon_id)
            .order_by(Winner.position)
            .all()
        )

        response = []

        for w in winners:
            submission = w.project
            team = submission.team

            response.append({
                "id": w.id,
                "position": w.position,
                "score": ScoringService.calculate_average(submission),
                "project": {
                    "id": submission.id,
                    "title": submission.project_title,
                    "github_url": submission.github_url,
                    "live_url": submission.live_url
                },
                "team": {
                    "id": team.id,
                    "name": team.name,
                    "members": [
                        {
                            "user_id": m.member_id,
                            "name": m.user.name,
                            "role": m.role.value
                        }
                        for m in team.members
                    ]
                },
                "created_at": w.created_at.isoformat()
            })

        return response
