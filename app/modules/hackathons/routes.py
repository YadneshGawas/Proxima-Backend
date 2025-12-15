from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from .services import HackathonService
from .schemas import HackathonCreateSchema,HackathonResponse, HackathonUpdateSchema,HackathonResponse


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
    status = request.args.get("status")


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
        search=search,
        status=status
        )

    results = [HackathonResponse.from_orm(h).dict() for h in hackathons]

    return jsonify({
        "page": page,
        "limit": limit,
        "total": total,
        "results": results
    }), 200

@hackathon_bp.route("/<hackathon_id>", methods=["PUT"])
@jwt_required()
def update_hackathon(hackathon_id):
    organizer_id = get_jwt_identity()
    payload = request.get_json()

    dto = HackathonUpdateSchema(**payload)

    hackathon = HackathonService.update_hackathon(
        hackathon_id=hackathon_id,
        organizer_id=organizer_id,
        data=dto
    )

    return jsonify(HackathonResponse.from_orm(hackathon).dict()), 200

@hackathon_bp.route("/<hackathon_id>", methods=["DELETE"])
@jwt_required()
def delete_hackathon(hackathon_id):
    organizer_id = get_jwt_identity()

    HackathonService.delete_hackathon(
        hackathon_id=hackathon_id,
        organizer_id=organizer_id
    )

    return jsonify({"message": "Hackathon deleted successfully."}), 200


@hackathon_bp.route("/view/<hackathon_id>", methods=["GET"])
@jwt_required(optional=True)
def get_hackathon(hackathon_id):
    user_id = get_jwt_identity()  # None if not logged in

    data = HackathonService.get_hackathon_by_id(
        hackathon_id=hackathon_id,
        user_id=user_id
    )

    return jsonify(data), 200



@hackathon_bp.route("/interest/<hackathon_id>", methods=["POST"])
@jwt_required()
def toggle_interest(hackathon_id):
    user_id = get_jwt_identity()

    result = HackathonService.toggle_interest(
        user_id=user_id,
        hackathon_id=hackathon_id
    )

    return jsonify(result), 200

