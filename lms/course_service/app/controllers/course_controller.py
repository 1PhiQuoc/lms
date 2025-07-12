from flask import request, jsonify
import psycopg2
import os
from datetime import datetime

# Cấu hình kết nối database
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'course_db'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'course_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres')
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def format_course_data(row):
    """Chuyển đổi dữ liệu từ database thành dictionary"""
    return {
        'id': row[0],
        'title': row[1],
        'description': row[2],
        'instructor_id': row[3],
        'created_at': row[4].isoformat() if row[4] else None,
        'updated_at': row[5].isoformat() if row[5] else None
    }

def get_courses():
    try:
        # Kết nối database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Thực hiện truy vấn
        cursor.execute("""
            SELECT id, title, description, instructor_id, created_at, updated_at
            FROM courses
            ORDER BY created_at DESC
        """)
        
        # Lấy kết quả và chuyển đổi thành list
        courses = []
        for row in cursor.fetchall():
            courses.append(format_course_data(row))
        
        # Đóng kết nối
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "data": courses,
            "message": "Lấy danh sách khóa học thành công"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Lỗi: {str(e)}"
        }), 500

def get_course(course_id):
    """Lấy thông tin một khóa học theo ID"""
    try:
        # Kết nối database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Thực hiện truy vấn
        cursor.execute("""
            SELECT id, title, description, instructor_id, created_at, updated_at
            FROM courses
            WHERE id = %s
        """, (course_id,))
        
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        # Kiểm tra kết quả
        if row:
            course = format_course_data(row)
            return jsonify({
                "success": True,
                "data": course,
                "message": "Lấy thông tin khóa học thành công"
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Không tìm thấy khóa học"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Lỗi: {str(e)}"
        }), 500

def create_course():
    """Tạo khóa học mới"""
    try:
        # Lấy dữ liệu từ request
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "Không có dữ liệu được gửi"
            }), 400
        
        # Kiểm tra các trường bắt buộc
        required_fields = ['title', 'description', 'instructor_id']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "message": f"Thiếu trường bắt buộc: {field}"
                }), 400
        
        # Kết nối database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Thêm khóa học mới
        cursor.execute("""
            INSERT INTO courses (title, description, instructor_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, title, description, instructor_id, created_at, updated_at
        """, (
            data['title'],
            data['description'],
            data['instructor_id'],
            datetime.now(),
            datetime.now()
        ))
        
        row = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        
        # Trả về kết quả
        course = format_course_data(row)
        return jsonify({
            "success": True,
            "data": course,
            "message": "Tạo khóa học thành công"
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Lỗi: {str(e)}"
        }), 500

def update_course(course_id):
    """Cập nhật thông tin khóa học"""
    try:
        # Lấy dữ liệu từ request
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "Không có dữ liệu được gửi"
            }), 400
        
        # Kết nối database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Xây dựng câu lệnh UPDATE
        update_parts = []
        values = []
        
        if 'title' in data:
            update_parts.append("title = %s")
            values.append(data['title'])
        
        if 'description' in data:
            update_parts.append("description = %s")
            values.append(data['description'])
        
        if 'instructor_id' in data:
            update_parts.append("instructor_id = %s")
            values.append(data['instructor_id'])
        
        # Nếu không có gì để cập nhật
        if not update_parts:
            cursor.close()
            conn.close()
            return jsonify({
                "success": False,
                "message": "Không có dữ liệu nào để cập nhật"
            }), 400
        
        # Thêm thời gian cập nhật
        update_parts.append("updated_at = %s")
        values.append(datetime.now())
        values.append(course_id)
        
        # Thực hiện cập nhật
        query = f"""
            UPDATE courses 
            SET {', '.join(update_parts)}
            WHERE id = %s
            RETURNING id, title, description, instructor_id, created_at, updated_at
        """
        
        cursor.execute(query, values)
        row = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        
        # Kiểm tra kết quả
        if row:
            course = format_course_data(row)
            return jsonify({
                "success": True,
                "data": course,
                "message": "Cập nhật khóa học thành công"
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Không tìm thấy khóa học"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Lỗi: {str(e)}"
        }), 500

def delete_course(course_id):
    try:
        # Kết nối database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Thực hiện xóa
        cursor.execute("DELETE FROM courses WHERE id = %s", (course_id,))
        deleted_count = cursor.rowcount
        
        conn.commit()
        cursor.close()
        conn.close()
        
        # Kiểm tra kết quả
        if deleted_count > 0:
            return jsonify({
                "success": True,
                "message": "Xóa khóa học thành công"
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Không tìm thấy khóa học"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Lỗi: {str(e)}"
        }), 500

def search_courses():
    """Tìm kiếm khóa học theo tên hoặc mô tả"""
    try:
        # Lấy từ khóa tìm kiếm
        query = request.args.get('q', '')
        if not query:
            return jsonify({
                "success": False,
                "message": "Cần nhập từ khóa tìm kiếm"
            }), 400
        
        # Kết nối database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Thực hiện tìm kiếm
        search_term = f"%{query}%"
        cursor.execute("""
            SELECT id, title, description, instructor_id, created_at, updated_at
            FROM courses
            WHERE title ILIKE %s OR description ILIKE %s
            ORDER BY created_at DESC
        """, (search_term, search_term))
        
        # Lấy kết quả
        courses = []
        for row in cursor.fetchall():
            courses.append(format_course_data(row))
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "data": courses,
            "message": "Tìm kiếm hoàn tất"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Lỗi: {str(e)}"
        }), 500
