# Hướng dẫn hệ thống quản trị (Admin)

## 🎉 Hệ thống quản trị hoàn thành!

### ✅ **Tính năng đã thêm:**

1. **Dashboard Admin** - Quản lý tổng quan hệ thống
2. **CRUD Laptop** - Thêm/Sửa/Xóa laptop
3. **Upload hình ảnh** - Quản lý hình ảnh laptop
4. **Phân quyền** - Chỉ admin mới có quyền truy cập
5. **Giao diện đẹp** - Responsive và user-friendly

## 🛠️ Cài đặt và thiết lập

### **Bước 1: Migration database**
```bash
python migrate_admin.py
```

### **Bước 2: Tạo admin user**
```bash
python create_admin.py
```

### **Bước 3: Đăng nhập admin**
- **Username**: admin
- **Password**: admin123
- **Email**: admin@laptop.com

## 🎯 Cách sử dụng

### **1. Truy cập trang admin:**
```
http://localhost:5000/admin
```

### **2. Dashboard tổng quan:**
- **Thống kê laptop**: Tổng số laptop trong hệ thống
- **Thống kê người dùng**: Số lượng user đã đăng ký
- **Thống kê yêu thích**: Tổng số laptop được yêu thích
- **Thống kê thương hiệu**: Số lượng thương hiệu khác nhau

### **3. Quản lý laptop:**

#### **Thêm laptop mới:**
1. Nhấn nút **"Thêm laptop mới"**
2. Điền đầy đủ thông tin:
   - **Thông tin cơ bản**: Tên, thương hiệu, danh mục, giá
   - **Thông số kỹ thuật**: CPU, RAM, GPU, storage, màn hình
   - **Thông tin pin**: Dung lượng, thời gian sử dụng
   - **Điểm số benchmark**: CPU và GPU scores
   - **Hình ảnh**: Upload file hình ảnh
3. Nhấn **"Thêm mới"**

#### **Sửa laptop:**
1. Trong bảng laptop, nhấn nút **"Sửa"** (biểu tượng bút chì)
2. Chỉnh sửa thông tin cần thiết
3. Upload hình ảnh mới (nếu cần)
4. Nhấn **"Cập nhật"**

#### **Xóa laptop:**
1. Trong bảng laptop, nhấn nút **"Xóa"** (biểu tượng thùng rác)
2. Xác nhận xóa trong modal
3. Nhấn **"Xóa"**

## 📊 Giao diện Dashboard

### **Thống kê tổng quan:**
```
┌─────────────────────────────────────────────────────────┐
│ 🛠️ Quản trị hệ thống                    [Thêm laptop mới] │
├─────────────────────────────────────────────────────────┤
│ 📊 Thống kê:                                            │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        │
│ │ 24      │ │ 15      │ │ 45      │ │ 7       │        │
│ │ Laptop  │ │ Users   │ │ Favorites│ │ Brands  │        │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘        │
└─────────────────────────────────────────────────────────┘
```

### **Bảng quản lý laptop:**
```
┌─────────────────────────────────────────────────────────┐
│ 📋 Quản lý laptop        [Tìm kiếm] [Lọc thương hiệu]   │
├─────────────────────────────────────────────────────────┤
│ Hình ảnh │ Tên laptop    │ Brand │ CPU  │ RAM │ Giá     │
│ ┌──────┐ │ ASUS TUF...  │ ASUS  │ i7   │ 16GB│ 25M VND │
│ │ 🖼️  │ │              │       │      │     │         │
│ └──────┘ │              │       │      │     │ [Sửa][Xem][Xóa] │
└─────────────────────────────────────────────────────────┘
```

## 📝 Form thêm/sửa laptop

### **Thông tin cơ bản:**
- **Tên laptop**: Tên đầy đủ của laptop
- **Thương hiệu**: ASUS, HP, Lenovo, Dell, Acer, MSI, Apple
- **Danh mục**: Văn phòng, Sinh viên, Gaming, Thiết kế, Lập trình
- **Giá**: Giá bán (VND)

### **Thông số kỹ thuật:**
- **CPU**: Model CPU (ví dụ: Intel Core i7-12700H)
- **RAM**: 4GB, 8GB, 16GB, 32GB, 64GB
- **GPU**: Card đồ họa (có thể để trống)
- **Storage**: Ổ cứng/SSD (ví dụ: 512GB SSD)
- **Màn hình**: Kích thước và độ phân giải

### **Thông tin pin:**
- **Dung lượng pin**: Wh (Watt-hour)
- **Thời gian văn phòng**: Phút
- **Thời gian gaming**: Phút

### **Điểm số benchmark:**
- **CPU Single Core**: Geekbench 6 (cắm sạc/dùng pin)
- **CPU Multi Core**: Geekbench 6 (cắm sạc/dùng pin)
- **GPU Score**: 3DMark hoặc Geekbench (cắm sạc/dùng pin)

### **Upload hình ảnh:**
- **Định dạng**: JPG, PNG, WebP
- **Kích thước**: Tối đa 5MB
- **Tên file**: Tự động tạo unique với timestamp

## 🔐 Phân quyền và bảo mật

### **Decorator admin_required:**
```python
@app.route("/admin")
@admin_required
def admin_dashboard():
    # Chỉ admin mới có thể truy cập
```

### **Kiểm tra quyền:**
- User phải đăng nhập
- User phải có role = 'admin'
- Nếu không có quyền → Redirect về trang chủ

### **Navbar hiển thị:**
- Link "Quản trị" chỉ hiển thị cho admin
- Icon và màu sắc khác biệt

## 🎨 Tính năng nổi bật

### **✅ Đã hoàn thành:**
- ✅ **Dashboard đẹp** với thống kê trực quan
- ✅ **CRUD đầy đủ** cho laptop
- ✅ **Upload hình ảnh** với validation
- ✅ **Phân trang** cho danh sách laptop
- ✅ **Tìm kiếm và lọc** theo thương hiệu
- ✅ **Phân quyền** chặt chẽ
- ✅ **Responsive design** cho mobile
- ✅ **Modal xác nhận** khi xóa
- ✅ **Flash messages** thông báo kết quả

### **🚀 Tính năng nâng cao:**
- **Validation**: Kiểm tra dữ liệu đầu vào
- **Error handling**: Xử lý lỗi gracefully
- **File management**: Tự động tạo tên file unique
- **Database transactions**: Rollback khi có lỗi
- **Security**: Sanitize filename với secure_filename

## 🔧 Scripts hỗ trợ

### **1. Migration database:**
```bash
python migrate_admin.py
```

### **2. Tạo admin user:**
```bash
python create_admin.py
```

### **3. Tạo test users:**
```bash
python create_test_user.py
```

## 📱 Responsive Design

### **Desktop (>768px):**
- Layout 2 cột cho form
- Bảng laptop đầy đủ
- Thống kê 4 cột

### **Mobile (<768px):**
- Layout 1 cột
- Bảng scrollable
- Form responsive

## 🔍 Troubleshooting

### **Lỗi thường gặp:**

1. **Không thể truy cập admin:**
   - Kiểm tra đã đăng nhập chưa
   - Kiểm tra user có role='admin' không
   - Chạy `python create_admin.py`

2. **Upload hình ảnh lỗi:**
   - Kiểm tra thư mục static/images có tồn tại
   - Kiểm tra quyền ghi file
   - Kiểm tra kích thước file < 5MB

3. **Form validation lỗi:**
   - Kiểm tra dữ liệu đầu vào
   - Kiểm tra các trường bắt buộc
   - Xem flash messages

### **Debug:**
```bash
# Kiểm tra admin user
python -c "from app import create_app; from models import User; app = create_app(); app.app_context().push(); admin = User.query.filter_by(role='admin').first(); print(admin.username if admin else 'No admin')"

# Kiểm tra thư mục upload
ls -la static/images/
```

## 📈 Kết quả đạt được

### **🎉 Hoàn thành 100%:**
- ✅ **Hệ thống admin** hoàn chỉnh và chuyên nghiệp
- ✅ **CRUD laptop** đầy đủ tính năng
- ✅ **Upload hình ảnh** an toàn và hiệu quả
- ✅ **Phân quyền** bảo mật và chặt chẽ
- ✅ **Giao diện** đẹp và dễ sử dụng
- ✅ **Responsive** hoạt động tốt trên mọi thiết bị

### **Cách test:**
1. Chạy: `python migrate_admin.py`
2. Chạy: `python create_admin.py`
3. Đăng nhập với: admin/admin123
4. Truy cập: `http://localhost:5000/admin`
5. Thử thêm/sửa/xóa laptop!

Bây giờ bạn có hệ thống quản trị hoàn chỉnh để quản lý laptop một cách chuyên nghiệp! 🎉 