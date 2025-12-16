from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.modules.submissions.schemas import (
    ProjectSubmissionCreateSchema,
    JudgeScoreCreateSchema,
    ProjectSubmissionResponseSchema,
    ProjectSubmissionUpdateSchema
)
from app.modules.submissions.services import (
    SubmissionService,
    ScoringService
)
from app.modules.submissions.models import ProjectSubmission
from app.modules.submissions.permission import require_judge_or_organizer
from app.modules.hackathons.models import Hackathon
from app.extensions import db

submission_bp = Blueprint("submissions", __name__)



@submission_bp.route("/hackathons/<hackathon_id>", methods=["POST"])
@jwt_required()
def submit_project(hackathon_id):
    data = ProjectSubmissionCreateSchema(**request.json)

    submission = SubmissionService.create_submission(
        hackathon_id,
        data.team_id,
        data
    )

    return jsonify({"id": submission.id}), 201


@submission_bp.route("/hackathons/<hackathon_id>", methods=["GET"])
@jwt_required()
def list_submissions(hackathon_id):
    user_id = get_jwt_identity()
    require_judge_or_organizer(user_id, hackathon_id)

    submissions = ProjectSubmission.query.filter_by(
        hackathon_id=hackathon_id
    ).all()

    response = []

    for s in submissions:
        team = s.team

        response.append({
            "id": s.id,
            "hackathon_id": s.hackathon_id,
            "project_title": s.project_title,
            "project_desc": s.project_desc,
            "github_url": s.github_url,
            "live_url": s.live_url,
            "created_at": s.created_at.isoformat(),
            "average_score": ScoringService.calculate_average(s),
            "team": {
                "id": team.id,
                "name": team.name,
                "created_by": team.created_by,
                "members": [
                    {
                        "user_id": m.member_id,          # ✅ correct column
                        "name": m.user.name,             # ✅ via relationship
                        "role": m.role.value,            # ✅ Enum → string
                        "joined_at": m.joined_at.isoformat()
                    }
                    for m in team.members
                ]
            }
        })

    return jsonify(response), 200


@submission_bp.route("/<submission_id>/score", methods=["POST"])
@jwt_required()
def score_submission(submission_id):
    user_id = get_jwt_identity()
    data = JudgeScoreCreateSchema(**request.json)

    submission = ProjectSubmission.query.get_or_404(submission_id)
    require_judge_or_organizer(user_id, submission.hackathon_id)

    ScoringService.submit_score(
        submission_id,
        user_id,
        data.score
    )

    return jsonify({"message": "Score saved"})

@submission_bp.route("/hackathons/<hackathon_id>/finalize", methods=["POST"])
@jwt_required()
def finalize_winners(hackathon_id):
    user_id = get_jwt_identity()
    hackathon = Hackathon.query.get_or_404(hackathon_id)

    if hackathon.organizer_id != user_id:
        return jsonify({"message": "Only organizer can finalize"}), 403

    submissions = ProjectSubmission.query.filter_by(
        hackathon_id=hackathon_id
    ).all()

    ranked = sorted(
        submissions,
        key=lambda s: ScoringService.calculate_average(s) or 0,
        reverse=True
    )

    winners = []
    for idx, sub in enumerate(ranked[:3], start=1):
        winners.append({
            "position": idx,
            "team": sub.team.name,
            "score": ScoringService.calculate_average(sub)
        })

    return jsonify(winners)


@submission_bp.route("/<submission_id>", methods=["GET"])
@jwt_required()
def get_submission(submission_id):
    user_id = get_jwt_identity()

    submission = ProjectSubmission.query.get_or_404(submission_id)
    require_judge_or_organizer(user_id, submission.hackathon_id)

    team = submission.team

    return jsonify({
        "id": submission.id,
        "hackathon_id": submission.hackathon_id,
        "project_title": submission.project_title,
        "project_desc": submission.project_desc,
        "github_url": submission.github_url,
        "live_url": submission.live_url,
        "created_at": submission.created_at.isoformat(),
        "average_score": ScoringService.calculate_average(submission),
        "team": {
            "id": team.id,
            "name": team.name,
            "created_by": team.created_by,
            "members": [
                {
                    "user_id": m.member_id,
                    "name": m.user.name,
                    "role": m.role.value,
                    "joined_at": m.joined_at.isoformat()
                }
                for m in team.members
            ]
        }
    }), 200

@submission_bp.route("/<submission_id>", methods=["PUT"])
@jwt_required()
def update_submission(submission_id):
    user_id = get_jwt_identity()
    data = ProjectSubmissionUpdateSchema(**request.json)

    submission = ProjectSubmission.query.get_or_404(submission_id)
    # 2️⃣ Extract hackathon_id FROM submission
    hackathon_id = submission.hackathon_id

    require_judge_or_organizer(user_id, hackathon_id)

    updated = SubmissionService.update_submission(submission, data)

    return jsonify({
        "id": updated.id,
        "message": "Submission updated successfully"
    }), 200

@submission_bp.route(
    "/hackathons/<hackathon_id>/my-submission",
    methods=["GET"]
)
@jwt_required()
def get_my_submission(hackathon_id):
    user_id = get_jwt_identity()

    submission = SubmissionService.get_my_submission(
        hackathon_id,
        user_id
    )

    team = submission.team

    return jsonify({
        "id": submission.id,
        "hackathon_id": submission.hackathon_id,
        "project_title": submission.project_title,
        "project_desc": submission.project_desc,
        "github_url": submission.github_url,
        "live_url": submission.live_url,
        "created_at": submission.created_at.isoformat(),
        "average_score": ScoringService.calculate_average(submission),
        "team": {
            "id": team.id,
            "name": team.name,
            "created_by": team.created_by,
            "members": [
                {
                    "user_id": m.member_id,
                    "name": m.user.name,
                    "role": m.role.value,
                    "joined_at": m.joined_at.isoformat()
                }
                for m in team.members
            ]
        }
    }), 200
