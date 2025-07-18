from ..models.user_model import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from .. import db
import random
import string

class UserProvider:
    @staticmethod
    def create_user(username, password):
        try:
            if UserProvider.get_user_by_username(username):
                return {"error": 1, "message": "Tên đăng nhập đã tồn tại"}
            user = User(
                username=username,
                password=generate_password_hash(password),
                code=UserProvider.generate_random_code()
            )
            db.session.add(user)
            db.session.commit()
            return {
                "error": 0,
                "message": "Đăng ký thành công",
                "data": {
                    "username": user.username,
                    "access_token": create_access_token(identity=user.id)
                }
            }
        except Exception as e:
            db.session.rollback()
            return str(e)
    def get_user_by_username(username):
        try:
            user = User.query.filter_by(username=username).first()
            if user:
                return user
            return None
        except Exception as e:
            return None
        
    def authenticate_user(username, password):
        user = UserProvider.get_user_by_username(username)
        if user and check_password_hash(user.password, password):
            return {
                "error": 0,
                "message": "Đăng nhập thành công",
                "data": {
                    "username": user.username,
                    "access_token": create_access_token(identity=user.id)
                }
            }
        else:
            return {
                "error": 1,
                "message": "Tên đăng nhập hoặc mật khẩu không đúng"
            }
    
    def generate_random_code(length=6):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    def get_user_profile():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user:
            return {
                "username": user.username,
                "code": user.code
            }
        return None
    
