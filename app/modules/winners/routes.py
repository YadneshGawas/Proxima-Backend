# app/modules/winners/routes.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.modules.hackathons.models import Hackathon
from app.modules.winners.services import WinnerService

winner_bp = Blueprint(
    "winners",
    __name__,
    url_prefix="/winners"
)


@winner_bp.route("/hackathons/<hackathon_id>/finalize", methods=["POST"])
@jwt_required()
def finalize_winners(hackathon_id):
    user_id = get_jwt_identity()
    hackathon = Hackathon.query.get_or_404(hackathon_id)

    if hackathon.organizer_id != user_id:
        return jsonify({"message": "Only organizer can finalize"}), 403

    winners = WinnerService.finalize_winners(hackathon)

    return jsonify({
        "message": "Winners finalized",
        "count": len(winners)
    }), 200


@winner_bp.route("/hackathons/<hackathon_id>", methods=["GET"])
@jwt_required(optional=True)
def list_winners(hackathon_id):
    winners = WinnerService.list_winners(hackathon_id)
    return jsonify(winners), 200
