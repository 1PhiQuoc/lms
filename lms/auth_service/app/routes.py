from flask import Blueprint
from .controllers import auth_controller

bp = Blueprint("auth", __name__)
bp.route("/register", methods=["POST"])(auth_controller.register)
bp.route("/login", methods=["POST"])(auth_controller.login)
