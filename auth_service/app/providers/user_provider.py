from ..models.user_model import User
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db

def create_user(username, password, role):
    user = User(username=username, role=role)
    user.password_hash = generate_password_hash(password)
    db.session.add(user)
    db.session.commit()
    return user

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def verify_password(user, password):
    return check_password_hash(user.password_hash, password)
