from flask import Blueprint, request, jsonify
from app.service.auth_service import register_service, login_service

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    return AuthService.login(data)

@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    return AuthService.register(data)
