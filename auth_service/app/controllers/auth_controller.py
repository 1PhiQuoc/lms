from flask import Blueprint, request, jsonify
from ..services.auth_service import AuthService

bp = Blueprint('auth', __name__)

# @bp.route('/login', methods=['POST'])
def login():
    data = request.json
    print("Login data received:", data)
    return AuthService.login(data)

# @bp.route('/register', methods=['POST'])
def register():
    data = request.json
    try:
        username = data.get("username")
        password = data.get("password")
        result = AuthService.register(username, password)
        if not result:
            return jsonify({"error": 1, "message": "Đăng ký thất bại"}), 400
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": 1, "message": str(e)}), 400
# @bp.route('/profile', methods=['GET'])
def profile():  
    try:
        user = AuthService.get_profile()
        if not user:
            return jsonify({"error": 1, "message": "Không tìm thấy người dùng"}), 404
        return jsonify(user), 200
    except Exception as e:
        return jsonify({"error": 1, "message": str(e)}), 400
# @bp.route('/refresh', methods=['POST'])
def refresh_token():
    try:
        new_token = AuthService.refresh_token()
        return jsonify({"token": new_token}), 200
    except Exception as e:
        return jsonify({"error": 1, "message": str(e)}), 400
