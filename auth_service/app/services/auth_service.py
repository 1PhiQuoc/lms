from ..providers import user_provider
from flask_jwt_extended import create_access_token

def register_service(data):
    user = user_provider.create_user(data['username'], data['password'], data['role'])
    return {"msg": "User registered", "user": user.username}

def login_service(data):
    user = user_provider.get_user_by_username(data['username'])
    if not user or not user_provider.verify_password(user, data['password']):
        return None
    token = create_access_token(identity={"id": user.id, "role": user.role})
    return {"access_token": token}
