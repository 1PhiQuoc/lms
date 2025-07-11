from flask import Blueprint, request, jsonify
from ..services.auth_service import AuthService

bp = Blueprint('auth', __name__)

# @bp.route('/login', methods=['POST'])
def login():
    data = request.json
    return AuthService.login(data)

# @bp.route('/register', methods=['POST'])
def register():
    data = request.json
    print("Registering user with data:", data)

    try:
        result = AuthService.register(data)
        return jsonify({
            "message": "User registered successfully",
            "user": result
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
