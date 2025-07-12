from ..providers.course_provider import CourseProvider

class CourseService:
    def __init__(self):
        self.provider = CourseProvider()
    
    def get_all_courses(self):
        """Get all courses"""
        return self.provider.get_all_courses()
    
    def get_course_by_id(self, course_id):
        """Get course by ID"""
        return self.provider.get_course_by_id(course_id)
    
    def create_course(self, course_data):
        """Create a new course"""
        return self.provider.create_course(course_data)
    
    def update_course(self, course_id, course_data):
        """Update an existing course"""
        return self.provider.update_course(course_id, course_data)
    
    def delete_course(self, course_id):
        """Delete a course"""
        return self.provider.delete_course(course_id)
    
    def search_courses(self, query):
        """Search courses by title or description"""
        return self.provider.search_courses(query)
