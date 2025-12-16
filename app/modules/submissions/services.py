from werkzeug.exceptions import BadRequest
from app.extensions import db
from app.modules.submissions.models import (
    ProjectSubmission,
    JudgeScore
)
from app.modules.teams.models import HackathonTeamMember


class SubmissionService:

    @staticmethod
    def create_submission(hackathon_id, team_id, data):
        existing = ProjectSubmission.query.filter_by(
            hackathon_id=hackathon_id,
            team_id=team_id
        ).first()

        if existing:
            raise BadRequest("Submission already exists")

        submission = ProjectSubmission(
            hackathon_id=hackathon_id,
            team_id=team_id,
            project_title=data.project_title,
            project_desc=data.project_desc,
            github_url=data.github_url,
            live_url=data.live_url
        )

        db.session.add(submission)
        db.session.commit()
        return submission

    @staticmethod
    def update_submission(submission, data):
        submission.project_title = data.project_title
        submission.project_desc = data.project_desc
        submission.github_url = data.github_url
        submission.live_url = data.live_url
        db.session.commit()
        return submission
    
    @staticmethod
    def get_my_submission(hackathon_id, user_id):
        # 1️⃣ Find teams where user is a member
        team_memberships = HackathonTeamMember.query.filter_by(
            member_id=user_id
        ).all()

        team_ids = [tm.hackathon_team_id for tm in team_memberships]

        if not team_ids:
            raise BadRequest("You are not part of any team for this hackathon")

        # 2️⃣ Find submission for this hackathon & user's team
        submission = (
            ProjectSubmission.query
            .filter(ProjectSubmission.hackathon_id == hackathon_id)
            .filter(ProjectSubmission.team_id.in_(team_ids))
            .first()
        )

        if not submission:
            raise BadRequest("No submission found for this hackathon")

        return submission


class ScoringService:

    @staticmethod
    def submit_score(submission_id, judge_id, score):
        if score < 0 or score > 100:
            raise BadRequest("Score must be between 0 and 100")

        existing = JudgeScore.query.filter_by(
            submission_id=submission_id,
            judge_id=judge_id
        ).first()

        if existing:
            existing.score = score
        else:
            existing = JudgeScore(
                submission_id=submission_id,
                judge_id=judge_id,
                score=score
            )
            db.session.add(existing)

        db.session.commit()
        return existing

    @staticmethod
    def calculate_average(submission):
        if not submission.scores:
            return None

        return round(
            sum(s.score for s in submission.scores) / len(submission.scores),
            2
        )

    