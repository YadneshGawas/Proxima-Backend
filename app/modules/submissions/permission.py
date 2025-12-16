from app.modules.hackathons.models import Hackathon
from app.modules.submissions.models import HackathonJudge
from werkzeug.exceptions import Forbidden


def require_judge_or_organizer(user_id, hackathon_id):
    hackathon = Hackathon.query.get(hackathon_id)

    if hackathon and hackathon.organizer_id == user_id:
        return

    judge = HackathonJudge.query.filter_by(
        hackathon_id=hackathon_id,
        user_id=user_id
    ).first()

    if not judge:
        raise Forbidden("You are not allowed to score this hackathon")