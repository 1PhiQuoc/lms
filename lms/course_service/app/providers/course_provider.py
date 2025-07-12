import psycopg2
import os
from datetime import datetime

class CourseProvider:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('DB_HOST', 'course_db'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'course_db'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'postgres')
        }
    
    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(**self.db_config)
    
    def get_all_courses(self):
        """Get all courses from database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, title, description, instructor_id, created_at, updated_at
                FROM courses
                ORDER BY created_at DESC
            """)
            
            courses = []
            for row in cursor.fetchall():
                courses.append({
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'instructor_id': row[3],
                    'created_at': row[4].isoformat() if row[4] else None,
                    'updated_at': row[5].isoformat() if row[5] else None
                })
            
            cursor.close()
            conn.close()
            return courses
        except Exception as e:
            print(f"Error getting all courses: {e}")
            return []
    
    def get_course_by_id(self, course_id):
        """Get course by ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, title, description, instructor_id, created_at, updated_at
                FROM courses
                WHERE id = %s
            """, (course_id,))
            
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if row:
                return {
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'instructor_id': row[3],
                    'created_at': row[4].isoformat() if row[4] else None,
                    'updated_at': row[5].isoformat() if row[5] else None
                }
            return None
        except Exception as e:
            print(f"Error getting course by ID: {e}")
            return None
    
    def create_course(self, course_data):
        """Create a new course"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO courses (title, description, instructor_id, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, title, description, instructor_id, created_at, updated_at
            """, (
                course_data['title'],
                course_data['description'],
                course_data['instructor_id'],
                datetime.now(),
                datetime.now()
            ))
            
            row = cursor.fetchone()
            conn.commit()
            cursor.close()
            conn.close()
            
            return {
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'instructor_id': row[3],
                'created_at': row[4].isoformat() if row[4] else None,
                'updated_at': row[5].isoformat() if row[5] else None
            }
        except Exception as e:
            print(f"Error creating course: {e}")
            return None
    
    def update_course(self, course_id, course_data):
        """Update an existing course"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Build update query dynamically
            update_fields = []
            values = []
            
            if 'title' in course_data:
                update_fields.append("title = %s")
                values.append(course_data['title'])
            
            if 'description' in course_data:
                update_fields.append("description = %s")
                values.append(course_data['description'])
            
            if 'instructor_id' in course_data:
                update_fields.append("instructor_id = %s")
                values.append(course_data['instructor_id'])
            
            if not update_fields:
                cursor.close()
                conn.close()
                return None
            
            update_fields.append("updated_at = %s")
            values.append(datetime.now())
            values.append(course_id)
            
            query = f"""
                UPDATE courses 
                SET {', '.join(update_fields)}
                WHERE id = %s
                RETURNING id, title, description, instructor_id, created_at, updated_at
            """
            
            cursor.execute(query, values)
            row = cursor.fetchone()
            conn.commit()
            cursor.close()
            conn.close()
            
            if row:
                return {
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'instructor_id': row[3],
                    'created_at': row[4].isoformat() if row[4] else None,
                    'updated_at': row[5].isoformat() if row[5] else None
                }
            return None
        except Exception as e:
            print(f"Error updating course: {e}")
            return None
    
    def delete_course(self, course_id):
        """Delete a course"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM courses WHERE id = %s", (course_id,))
            deleted_count = cursor.rowcount
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return deleted_count > 0
        except Exception as e:
            print(f"Error deleting course: {e}")
            return False
    
    def search_courses(self, query):
        """Search courses by title or description"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            search_term = f"%{query}%"
            cursor.execute("""
                SELECT id, title, description, instructor_id, created_at, updated_at
                FROM courses
                WHERE title ILIKE %s OR description ILIKE %s
                ORDER BY created_at DESC
            """, (search_term, search_term))
            
            courses = []
            for row in cursor.fetchall():
                courses.append({
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'instructor_id': row[3],
                    'created_at': row[4].isoformat() if row[4] else None,
                    'updated_at': row[5].isoformat() if row[5] else None
                })
            
            cursor.close()
            conn.close()
            return courses
        except Exception as e:
            print(f"Error searching courses: {e}")
            return []
