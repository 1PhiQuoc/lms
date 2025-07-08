from flask import request, jsonify
from ..services.auth_service import register_service, login_service

def register():
    data = request.get_json()
    print("Received data for registration:", data)
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"msg": "Missing username or password"}), 400
    if len(data['password']) < 6:
        return jsonify({"msg": "Password must be at least 6 characters long"}), 400
    result = register_service(data)
    return jsonify(result), 201

def login():
    data = request.get_json()
    result = login_service(data)
    if not result:
        return jsonify({"msg": "Invalid credentials"}), 401
    return jsonify(result)
