from flask import Blueprint
from .controllers.course_controller import (
    get_courses, get_course, create_course, 
    update_course, delete_course, search_courses
)

bp = Blueprint("course", __name__)

# CRUD operations
bp.route("/courses", methods=["GET"])(get_courses)
bp.route("/courses/<int:course_id>", methods=["GET"])(get_course)
bp.route("/courses", methods=["POST"])(create_course)
bp.route("/courses/<int:course_id>", methods=["PUT"])(update_course)
bp.route("/courses/<int:course_id>", methods=["DELETE"])(delete_course)

# Search
bp.route("/courses/search", methods=["GET"])(search_courses)
