from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from .services import HackathonService
from .schemas import HackathonCreateSchema,HackathonResponse 

hackathon_bp = Blueprint("hackathons", __name__)

@hackathon_bp.route("/",methods=['GET'])
def check_hackathon():
    return jsonify("This is home Hackathon route")

@hackathon_bp.route("/create", methods=["POST"])
@jwt_required()
def create_hackathon():
    payload = request.get_json()

    # Auto-inject organizer from JWT
    payload["organizer_id"] = get_jwt_identity()

    data = HackathonCreateSchema(**payload)

    hackathon = HackathonService.create_hackathon(data)

    return jsonify(HackathonResponse.from_orm(hackathon).dict()), 201

@hackathon_bp.route("/all", methods=["GET"])
@jwt_required(optional=True)
def list_hackathons():

    # Query params
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    mode = request.args.get("mode")
    participation_type = request.args.get("participation_type")
    tag = request.args.get("tag")
    search = request.args.get("search")


   # If ?mine=true → fetch hackathons created by this user
    mine = request.args.get("mine", "false").lower() == "true"
    organizer_id = get_jwt_identity() if mine else None

    hackathons, total = HackathonService.get_hackathons(
        organizer_id=organizer_id,
        page=page,
        limit=limit,
        mode=mode,
        participation_type=participation_type,
        tag=tag,
        search=search
        )

    results = [HackathonResponse.from_orm(h).dict() for h in hackathons]

    return jsonify({
        "page": page,
        "limit": limit,
        "total": total,
        "results": results
    }), 200