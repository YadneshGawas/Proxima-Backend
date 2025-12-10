from flask import Blueprint, request, jsonify
from .services import AuthService
from .schemas import (RegisterSchema,LoginSchema,RegisterResponse, LoginResponse, LogoutResponse,UserResponse)
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/test', methods=['GET'])
def test():
    return "User module is working fine."

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        validated_data = RegisterSchema(**data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    try:
        response, status_code = AuthService.register_user(
            name=validated_data.name,
            email=validated_data.email,
            password=validated_data.password
        )
        return jsonify(RegisterResponse(**response).model_dump()), status_code
    except Exception as e:
        return jsonify({"message": "Invalid input", "errors": e.errors()}), 400
    
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        validated_data = LoginSchema(**data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    try:
        response, status_code = AuthService.login_user(
            email=validated_data.email,
            password=validated_data.password
        )
        return jsonify(LoginResponse(**response).model_dump()), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@auth_bp.route('/logout', methods=['GET'])
def logout():
    try:
        response, status_code = AuthService.logout_user()
        return jsonify(LogoutResponse(**response).model_dump()), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    try:
        user, status_code = AuthService.get_current_user(user_id)
        user_response = UserResponse(
            id=user['id'],
            name=user['name'],
            email=user['email']
        )
        return jsonify(user_response.model_dump()), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@auth_bp.route('/update', methods=['PUT'])
@jwt_required() 
def update_user():
    user_id = get_jwt_identity()
    data = request.get_json()
    try:
        response, status_code = AuthService.update_user(user_id, data)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 400  
    
    
