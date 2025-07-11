from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.course_service import list_courses, create_course, delete_course

@jwt_required()
def get_courses():
    return jsonify(list_courses())

def get_course():
    return jsonify(list_courses())

@jwt_required()
def create():
    user = get_jwt_identity()
    data = request.get_json()
    result = create_course(data, user)
    return jsonify(result), 201 if isinstance(result, dict) else result[1]

@jwt_required()
def delete(course_id):
    user = get_jwt_identity()
    result = delete_course(course_id, user)
    return jsonify(result), 200 if isinstance(result, dict) else result[1]
