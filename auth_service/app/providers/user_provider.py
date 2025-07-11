from ..models.user_model import User
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db
import random
import string

class UserProvider:
    @staticmethod
    def authenticate_user(data):
        pass
    
    @staticmethod
    def create_user(username, password):
        try:
            user = User(
                username=username,
                password=generate_password_hash(password),
                code=UserProvider.generate_random_code()
            )
            db.session.add(user)
            db.session.commit()
            return user
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
        
    def login_user(username, password):
        user = UserProvider.get_user_by_username(username)
        if user and check_password_hash(user.password, password):
            return user
        return None
    
    def generate_random_code(length=6):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
