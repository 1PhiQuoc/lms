import os
from flask import request, jsonify, g

def secret_key(app):
    @app.before_request
    def check_secret_token():
        secret = os.getenv("SECRET_KEY")
        bypass_paths = ['/login', '/register']
        headerSecret = request.headers.get("token")
        if request.path not in bypass_paths:
                return
       
        if headerSecret is None or headerSecret != secret:
                return jsonify({"message": "Không hợp lệ vui lòng kiểm tra thông tin!"}), 401
   
