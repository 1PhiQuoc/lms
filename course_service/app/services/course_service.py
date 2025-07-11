from ..providers import course_provider

def list_courses():
    courses = course_provider.get_all_courses()
    return [{"id": c.id, "title": c.title} for c in courses]

def create_course(data, user):
    if user['role'] != 'teacher':
        return {"msg": "Only teachers can create courses"}, 403
    course = course_provider.create_course(data['title'], data.get('description'), user['id'])
    return {"msg": "Created", "id": course.id}

def delete_course(course_id, user):
    course = course_provider.get_course_by_id(course_id)
    if not course:
        return {"msg": "Not found"}, 404
    if course.teacher_id != user['id']:
        return {"msg": "Unauthorized"}, 403
    course_provider.delete_course(course)
    return {"msg": "Deleted"}
