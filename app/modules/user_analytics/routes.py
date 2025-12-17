from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.modules.user_analytics.services import UserAnalyticsService

user_analytics_bp = Blueprint(
    "user_analytics",
    __name__,
    url_prefix="/users/analytics"
)


@user_analytics_bp.route("/me", methods=["GET"])
@jwt_required()
def my_analytics():
    user_id = get_jwt_identity()

    data = UserAnalyticsService.get_user_analytics(user_id)
    print(data)

    return jsonify(data), 200
