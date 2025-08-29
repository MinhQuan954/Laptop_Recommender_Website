# Laptop Recommender (Flask + SQLite)

## Cách chạy trên localhost
1. Tạo virtualenv và cài dependency:
```
pip install -r requirements.txt
```
2. Khởi tạo & seed dữ liệu mẫu:
```
python seed.py
```
3. Chạy ứng dụng:
```
python app.py
```
4. Truy cập: http://127.0.0.1:5000

## Tính năng đã có (MVP)
- Danh sách, chi tiết laptop
- Tìm kiếm & lọc theo hãng/giá/RAM
- Gợi ý theo nhu cầu + ngân sách
- So sánh nhiều laptop (thêm id vào query)
- Đăng ký/Đăng nhập (Flask-Login)
- Yêu thích (Favorites) cho user

## Ghi chú
- Mặc định dùng SQLite (file `app.db`). Có thể đổi sang SQL Server qua biến môi trường `DATABASE_URL`.
- Dữ liệu mẫu nằm trong `seed.py` – chỉnh sửa/nhân bản theo nhu cầu.
