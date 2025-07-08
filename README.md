# 🧠 LMS Microservices - Flask Clean Architecture

## 📦 Services
- `auth_service`: Đăng ký / đăng nhập bằng JWT
- `course_service`: CRUD khóa học (phải xác thực)
- Áp dụng mô hình `Controller - Service - Provider - Model`
- Chạy bằng Docker

## 🚀 Cách chạy
```bash
docker-compose up --build
docker-compose exec auth_service flask db upgrade
docker-compose exec course_service flask db upgrade
```

## 🔐 Gọi API
```http
POST /register
POST /login → trả JWT token
Authorization: Bearer <token>
```
