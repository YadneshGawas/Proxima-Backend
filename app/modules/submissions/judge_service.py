from werkzeug.exceptions import BadRequest
from app.extensions import db
from app.modules.submissions.models import HackathonJudge
from app.modules.users.models import User

class JudgeService:

    @staticmethod
    def assign_judge(hackathon_id: str, user_id: int):
        existing = HackathonJudge.query.filter_by(
            hackathon_id=hackathon_id,
            user_id=user_id
        ).first()

        if existing:
            raise BadRequest("User is already a judge")

        judge = HackathonJudge(
            hackathon_id=hackathon_id,
            user_id=user_id
        )

        db.session.add(judge)
        db.session.commit()

        user = User.query.get(user_id)
        return judge,user

    @staticmethod
    def remove_judge(hackathon_id: str, user_id: int):
        judge = HackathonJudge.query.filter_by(
            hackathon_id=hackathon_id,
            user_id=user_id
        ).first()

        if not judge:
            raise BadRequest("Judge not found")

        db.session.delete(judge)
        db.session.commit()

    @staticmethod
    def list_judges(hackathon_id: str):
         return (
            db.session.query(HackathonJudge, User)
            .join(User, User.id == HackathonJudge.user_id)
            .filter(HackathonJudge.hackathon_id == hackathon_id)
            .all()
        )
