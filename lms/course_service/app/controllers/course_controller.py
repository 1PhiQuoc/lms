from flask import request, jsonify
import psycopg2
import os
from datetime import datetime

DB_CONFIG = {
    'host': 'course_db',
    'port': '5432',
    'database': 'course_db',
    'user': 'postgres',
    'password': 'postgres'
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def format_course_data(row):
    return {
        'id': row[0],
        'title': row[1],
        'description': row[2],
        'instructor_id': row[3],
        'created_at': str(row[4]) if row[4] else None,
        'updated_at': str(row[5]) if row[5] else None
    }

def get_all_courses():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = """
            SELECT id, title, description, instructor_id, created_at, updated_at
            FROM courses
            ORDER BY created_at DESC
        """
        cursor.execute(sql)
        
        result = cursor.fetchall()
        
        courses = []
        for row in result:
            course = format_course_data(row)
            courses.append(course)
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "data": courses,
            "message": "Get courses successfully"
        }), 200
        
    except Exception as error:
        return jsonify({
            "success": False,
            "message": f"Error: {str(error)}"
        }), 500

def get_course_by_id(course_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = """
            SELECT id, title, description, instructor_id, created_at, updated_at
            FROM courses
            WHERE id = %s
        """
        cursor.execute(sql, (course_id,))
        
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result:
            course = format_course_data(result)
            return jsonify({
                "success": True,
                "data": course,
                "message": "Course found"
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Course not found"
            }), 404
            
    except Exception as error:
        return jsonify({
            "success": False,
            "message": f"Error: {str(error)}"
        }), 500

def create_new_course():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "message": "No data provided"
            }), 400
        
        if 'title' not in data:
            return jsonify({
                "success": False,
                "message": "Missing course title"
            }), 400
            
        if 'description' not in data:
            return jsonify({
                "success": False,
                "message": "Missing course description"
            }), 400
            
        if 'instructor_id' not in data:
            return jsonify({
                "success": False,
                "message": "Missing instructor ID"
            }), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = """
            INSERT INTO courses (title, description, instructor_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, title, description, instructor_id, created_at, updated_at
        """
        
        current_time = datetime.now()
        cursor.execute(sql, (
            data['title'],
            data['description'],
            data['instructor_id'],
            current_time,
            current_time
        ))
        
        result = cursor.fetchone()
        conn.commit()
        
        cursor.close()
        conn.close()
        
        new_course = format_course_data(result)
        return jsonify({
            "success": True,
            "data": new_course,
            "message": "Course created successfully"
        }), 201
        
    except Exception as error:
        return jsonify({
            "success": False,
            "message": f"Error: {str(error)}"
        }), 500

def update_course(course_id):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "message": "No data to update"
            }), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        update_fields = []
        values = []
        
        if 'title' in data:
            update_fields.append("title = %s")
            values.append(data['title'])
        
        if 'description' in data:
            update_fields.append("description = %s")
            values.append(data['description'])
        
        if 'instructor_id' in data:
            update_fields.append("instructor_id = %s")
            values.append(data['instructor_id'])
        
        if not update_fields:
            cursor.close()
            conn.close()
            return jsonify({
                "success": False,
                "message": "No data to update"
            }), 400
        
        update_fields.append("updated_at = %s")
        values.append(datetime.now())
        values.append(course_id)
        
        sql = f"""
            UPDATE courses 
            SET {', '.join(update_fields)}
            WHERE id = %s
            RETURNING id, title, description, instructor_id, created_at, updated_at
        """
        
        cursor.execute(sql, values)
        result = cursor.fetchone()
        conn.commit()
        
        cursor.close()
        conn.close()
        
        if result:
            updated_course = format_course_data(result)
            return jsonify({
                "success": True,
                "data": updated_course,
                "message": "Course updated successfully"
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Course not found"
            }), 404
            
    except Exception as error:
        return jsonify({
            "success": False,
            "message": f"Error: {str(error)}"
        }), 500

def delete_course(course_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = "DELETE FROM courses WHERE id = %s"
        cursor.execute(sql, (course_id,))
        
        deleted_count = cursor.rowcount
        
        conn.commit()
        cursor.close()
        conn.close()
        
        if deleted_count > 0:
            return jsonify({
                "success": True,
                "message": "Course deleted successfully"
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Course not found"
            }), 404
            
    except Exception as error:
        return jsonify({
            "success": False,
            "message": f"Error: {str(error)}"
        }), 500

def search_courses():
    try:
        query = request.args.get('q', '')
        
        if not query:
            return jsonify({
                "success": False,
                "message": "Search query required"
            }), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        search_term = f"%{query}%"
        sql = """
            SELECT id, title, description, instructor_id, created_at, updated_at
            FROM courses
            WHERE title ILIKE %s OR description ILIKE %s
            ORDER BY created_at DESC
        """
        cursor.execute(sql, (search_term, search_term))
        
        result = cursor.fetchall()
        
        search_results = []
        for row in result:
            course = format_course_data(row)
            search_results.append(course)
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "data": search_results,
            "message": f"Found {len(search_results)} courses"
        }), 200
        
    except Exception as error:
        return jsonify({
            "success": False,
            "message": f"Error: {str(error)}"
        }), 500


