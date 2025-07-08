from flask import Blueprint
from .controllers import course_controller

bp = Blueprint("course", __name__)
bp.route("/courses", methods=["GET"])(course_controller.get_courses)
bp.route("/courses", methods=["POST"])(course_controller.create)
bp.route("/courses/<int:course_id>", methods=["DELETE"])(course_controller.delete)
