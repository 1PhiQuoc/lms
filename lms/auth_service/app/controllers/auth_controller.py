from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    return AuthService.login(data)

@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    return AuthService.register(data)
