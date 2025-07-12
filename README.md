<<<<<<< HEAD
# lms_flutter

A new Flutter project.

## Getting Started

This project is a starting point for a Flutter application.

A few resources to get you started if this is your first Flutter project:

- [Lab: Write your first Flutter app](https://docs.flutter.dev/get-started/codelab)
- [Cookbook: Useful Flutter samples](https://docs.flutter.dev/cookbook)

For help getting started with Flutter development, view the
[online documentation](https://docs.flutter.dev/), which offers tutorials,
samples, guidance on mobile development, and a full API reference.
=======
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
>>>>>>> 97e544cca8db600f665ca0ac03a0a5149d2a230f
