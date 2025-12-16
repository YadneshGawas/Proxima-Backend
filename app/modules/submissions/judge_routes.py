from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.modules.hackathons.models import Hackathon
from app.modules.submissions.judge_service import JudgeService
from app.modules.submissions.schemas import JudgeAssignSchema
from app.modules.submissions.models import HackathonJudge

judge_bp = Blueprint(
    "judges",
    __name__,
    url_prefix="/hackathons/<hackathon_id>/judges"
)


@judge_bp.route("/", methods=["POST"])
@jwt_required()
def assign_judge(hackathon_id):
    user_id = get_jwt_identity()
    data = JudgeAssignSchema(**request.json)

    hackathon = Hackathon.query.get_or_404(hackathon_id)

    if hackathon.organizer_id != user_id:
        return jsonify({"message": "Only organizer can assign judges"}), 403

    judge, user = JudgeService.assign_judge(
        hackathon_id,
        data.user_id
    )

    return jsonify({
        "user_id": judge.user_id,
        "name": user.name
    }), 201


@judge_bp.route("/", methods=["GET"])
@jwt_required()
def list_judges(hackathon_id):
    rows = JudgeService.list_judges(hackathon_id)

    return jsonify([
        {
            "user_id": judge.user_id,
            "name": user.name
        }
        for judge, user in rows
    ])


@judge_bp.route("/<int:judge_user_id>", methods=["DELETE"])
@jwt_required()
def remove_judge(hackathon_id, judge_user_id):
    user_id = get_jwt_identity()
    hackathon = Hackathon.query.get_or_404(hackathon_id)

    if hackathon.organizer_id != user_id:
        return jsonify({"message": "Only organizer can remove judges"}), 403

    JudgeService.remove_judge(hackathon_id, judge_user_id)

    return jsonify({"message": "Judge removed"})
