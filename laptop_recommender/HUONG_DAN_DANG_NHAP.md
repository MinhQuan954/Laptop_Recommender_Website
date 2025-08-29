# Hướng dẫn sử dụng hệ thống đăng nhập/đăng ký

## 🚀 Tính năng đã có

### ✅ **Đăng ký tài khoản**
- Form đăng ký hiện đại với validation
- Kiểm tra username và email trùng lặp
- Validation mật khẩu (tối thiểu 6 ký tự)
- Xác nhận mật khẩu
- Hiển thị lợi ích khi đăng ký

### ✅ **Đăng nhập**
- Form đăng nhập đẹp mắt
- Hiển thị/ẩn mật khẩu
- Validation thông tin đăng nhập
- Redirect về trang trước đó
- Thông báo chào mừng cá nhân hóa

### ✅ **Quản lý tài khoản**
- Dropdown menu người dùng
- Trang hồ sơ cá nhân
- Thống kê laptop yêu thích
- Timeline hoạt động
- Đăng xuất an toàn

## 👥 **Tài khoản test có sẵn**

| Username | Email | Password |
|----------|-------|----------|
| admin | admin@example.com | admin123 |
| user1 | user1@example.com | user123 |
| test | test@example.com | test123 |

## 🔧 **Cách sử dụng**

### **1. Đăng ký tài khoản mới:**
1. Click "Đăng ký" trên navbar
2. Điền thông tin:
   - **Tên đăng nhập**: 3-20 ký tự
   - **Email**: Địa chỉ email hợp lệ
   - **Mật khẩu**: Tối thiểu 6 ký tự
   - **Xác nhận mật khẩu**: Nhập lại mật khẩu
3. Click "Tạo tài khoản"

### **2. Đăng nhập:**
1. Click "Đăng nhập" trên navbar
2. Nhập username và mật khẩu
3. Click "Đăng nhập"
4. Hệ thống sẽ chào mừng bạn

### **3. Sử dụng tài khoản:**
- **Hồ sơ**: Xem thông tin cá nhân và thống kê
- **Yêu thích**: Lưu và quản lý laptop yêu thích
- **So sánh**: Chọn nhiều laptop để so sánh
- **Đăng xuất**: Thoát khỏi tài khoản

## 🎨 **Giao diện**

### **Trang đăng nhập:**
- Header màu xanh với icon
- Form lớn, dễ nhìn
- Nút hiển thị/ẩn mật khẩu
- Link chuyển đến đăng ký
- Thông tin lợi ích

### **Trang đăng ký:**
- Header màu xanh lá
- Validation real-time
- Hướng dẫn từng trường
- Xác nhận mật khẩu
- Hiển thị lợi ích khi đăng ký

### **Navbar:**
- Nút đăng nhập/đăng ký đẹp mắt
- Dropdown menu cho user đã đăng nhập
- Icon và màu sắc phù hợp

## 🔒 **Bảo mật**

### **Validation:**
- Username: 3-20 ký tự
- Email: Định dạng hợp lệ
- Password: Tối thiểu 6 ký tự
- Kiểm tra trùng lặp username/email

### **Mật khẩu:**
- Hash bằng werkzeug.security
- Không lưu plain text
- Validation client-side và server-side

### **Session:**
- Sử dụng Flask-Login
- Session an toàn
- Tự động logout khi đóng trình duyệt

## 🛠️ **Tính năng nâng cao**

### **Trang hồ sơ:**
- Thông tin cá nhân
- Thống kê laptop yêu thích
- Timeline hoạt động
- Quản lý laptop yêu thích

### **Validation nâng cao:**
- Kiểm tra độ mạnh mật khẩu
- Validation email format
- Thông báo lỗi chi tiết
- Real-time feedback

### **UX/UI:**
- Responsive design
- Icon Font Awesome
- Animation và transition
- Color scheme nhất quán

## 📱 **Responsive**

- Hoạt động tốt trên mobile
- Form tự động điều chỉnh kích thước
- Touch-friendly buttons
- Optimized cho tablet

## 🔧 **Tùy chỉnh**

### **Thêm validation:**
```python
# Trong app.py, route register
if len(password) < 8:
    errors.append("Mật khẩu phải có ít nhất 8 ký tự")

if not any(c.isupper() for c in password):
    errors.append("Mật khẩu phải có ít nhất 1 chữ hoa")
```

### **Thêm trường thông tin:**
```python
# Trong models.py
class User(UserMixin, db.Model):
    # Thêm trường mới
    phone = db.Column(db.String(15))
    address = db.Column(db.String(200))
```

### **Tùy chỉnh giao diện:**
- Thay đổi màu sắc trong CSS
- Thêm animation
- Tùy chỉnh icon
- Thay đổi layout

## 🚨 **Xử lý lỗi**

### **Lỗi thường gặp:**
1. **Username đã tồn tại**: Chọn tên khác
2. **Email không hợp lệ**: Kiểm tra định dạng
3. **Mật khẩu quá ngắn**: Tối thiểu 6 ký tự
4. **Mật khẩu không khớp**: Nhập lại chính xác

### **Debug:**
- Kiểm tra console browser
- Xem log Flask
- Kiểm tra database
- Test từng bước

## 📈 **Phát triển tiếp**

### **Tính năng có thể thêm:**
- Quên mật khẩu
- Xác thực email
- Đăng nhập bằng Google/Facebook
- Two-factor authentication
- Profile picture
- Thay đổi mật khẩu
- Xóa tài khoản

### **Cải thiện:**
- Thêm captcha
- Rate limiting
- Log hoạt động
- Backup database
- Performance optimization 