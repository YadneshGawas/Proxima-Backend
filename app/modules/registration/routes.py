from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError

from app.modules.registration.schemas import (
    RegistrationCreateSchema,
    RegistrationResponseSchema
)
from app.modules.registration.services import RegistrationService

registration_bp = Blueprint(
    "registrations",
    __name__
)


@registration_bp.route("/", methods=["POST"])
@jwt_required()
def register():
    payload = RegistrationCreateSchema(**request.json)
    user_id = get_jwt_identity()

    registration = RegistrationService.register(
        hackathon_id=payload.hackathon_id,
        user_id=user_id,
        team_id=payload.team_id
    )

    response = RegistrationResponseSchema.from_orm(registration)
    return jsonify(response.dict()), 201

@registration_bp.route("/<registration_id>/status", methods=["PATCH"])
@jwt_required()
def update_status(registration_id):
    status = request.json.get("status")

    if status not in ("approved", "rejected"):
        return jsonify({"error": "Invalid status"}), 400

    registration = RegistrationService.update_status(
        registration_id=registration_id,
        status=status
    )

    response = RegistrationResponseSchema.from_orm(registration)
    return jsonify(response.dict()), 200

@registration_bp.route("/me", methods=["GET"])
@jwt_required()
def my_registrations():
    user_id = get_jwt_identity()
    registrations = RegistrationService.get_user_registrations(user_id)

    response = [
        RegistrationResponseSchema.from_orm(r).dict()
        for r in registrations
    ]

    return jsonify(response), 200

@registration_bp.route("/team/<team_id>", methods=["GET"])
@jwt_required()
def team_registrations(team_id):
    registrations = RegistrationService.get_team_registrations(team_id)

    response = [
        RegistrationResponseSchema.from_orm(r).dict()
        for r in registrations
    ]

    return jsonify(response), 200

@registration_bp.route("/hackathon/<hackathon_id>", methods=["GET"])
@jwt_required()
def hackathon_registrations(hackathon_id):
    registrations = RegistrationService.get_hackathon_registrations(hackathon_id)

    response = [
        RegistrationResponseSchema.from_orm(r).dict()
        for r in registrations
    ]

    return jsonify(response), 200

@registration_bp.route("/check/<hackathon_id>", methods=["GET"])
@jwt_required()
def check_registration(hackathon_id):
    user_id = get_jwt_identity()

    result = RegistrationService.check_user_registration(
        hackathon_id=hackathon_id,
        user_id=user_id
    )

    return jsonify(result), 200

@registration_bp.route("/analytics/<hackathon_id>", methods=["GET"])
@jwt_required()
def hackathon_analytics(hackathon_id):
    analytics = RegistrationService.get_hackathon_analytics(hackathon_id)
    return jsonify(analytics), 200