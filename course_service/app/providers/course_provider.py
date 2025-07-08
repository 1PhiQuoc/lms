from ..models.course_model import Course
from .. import db

def create_course(title, description, teacher_id):
    course = Course(title=title, description=description, teacher_id=teacher_id)
    db.session.add(course)
    db.session.commit()
    return course

def get_all_courses():
    return Course.query.all()

def get_course_by_id(course_id):
    return Course.query.get(course_id)

def delete_course(course):
    db.session.delete(course)
    db.session.commit()
