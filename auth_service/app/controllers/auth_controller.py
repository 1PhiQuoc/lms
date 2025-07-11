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
    try:
        username = data.get("username")
        password = data.get("password")
        result = AuthService.register(username, password)
        if not result:
            return jsonify({"error": "Đăng ký thất bại"}), 400
        return jsonify({
            "message": "Đăng ký thành công",
            "user": result
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
