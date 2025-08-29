# Hướng dẫn cập nhật hình ảnh laptop

## 🎉 Kết quả đã đạt được

### ✅ **Hoàn thành 100%**
- **24/24 laptop** đã có hình ảnh thật
- **0 placeholder** còn lại
- **0 laptop** thiếu hình ảnh

## 📁 Cấu trúc thư mục

```
laptop_recommender/
├── static/
│   └── images/
│       ├── tuff15_1.webp          # ASUS TUF Gaming F15
│       ├── victus16_1.webp        # HP Victus 16
│       ├── msikatana15_1.webp     # MSI Katana 15
│       ├── legion5_1.webp         # Lenovo Legion 5
│       ├── creator16_1.webp       # MSI Creator M16
│       ├── proartstudiobook_1.webp # ASUS ProArt StudioBook
│       ├── xps15_1.webp           # Dell XPS 15
│       ├── macbookpro14m3_1.webp  # MacBook Pro 14 M3
│       ├── acerswiftgo14_1.webp   # Acer Swift Go 14
│       ├── thinkpadx1_1.webp      # Lenovo ThinkPad X1
│       ├── dellprecision5570_1.webp # Dell Precision 5570
│       ├── zbookstu_1.webp        # HP ZBook Studio
│       ├── aspire7a715_1.webp     # Acer Aspire 7 A715
│       ├── air13M2_1.webp         # MacBook Air 13 M2
│       ├── asusvivobook15_1.webp  # ASUS VivoBook 15
│       ├── ideapad3_1.webp        # Lenovo IdeaPad 3
│       ├── Dellinspiron14_1.webp  # Dell Inspiron 14
│       ├── ideapad5_1.webp        # Lenovo IdeaPad 5
│       ├── Pavilion14_1.webp      # HP Pavilion 14
│       ├── aspire3_1.webp         # Acer Aspire 3
│       ├── asusE410_1.webp        # ASUS E410
│       ├── lenovoIdeaPad_1.webp   # Lenovo IdeaPad 1
│       ├── HP15s_1.webp           # HP 15s
│       └── Aspire1_1.webp         # Acer Aspire 1
```

## 🛠️ Scripts có sẵn

### **1. `update_images_auto.py` - Script chính**
```bash
python update_images_auto.py
```

**Tính năng:**
- Tự động map hình ảnh theo tên laptop
- Hỗ trợ nhiều định dạng (.webp, .jpg, .png, .jpeg)
- Mapping thông minh theo từ khóa
- Thống kê chi tiết kết quả

**Cách sử dụng:**
1. Chạy script
2. Chọn option 1: "Tự động cập nhật hình ảnh"
3. Xem kết quả và thống kê

### **2. `check_images.py` - Kiểm tra kết quả**
```bash
python check_images.py
```

**Tính năng:**
- Hiển thị trạng thái hình ảnh của tất cả laptop
- Thống kê chi tiết
- Đánh giá chất lượng

### **3. `them_hinh_anh.py` - Thêm hình ảnh thủ công**
```bash
python them_hinh_anh.py
```

**Tính năng:**
- Thêm hình ảnh cho từng laptop cụ thể
- Kiểm tra file tồn tại
- Cập nhật database

## 🔍 Thuật toán mapping

### **Mapping chính xác:**
```python
mappings = {
    'asustufgamingf15': ['tuff15_1.webp', 'tuff15_2.webp'],
    'hpvictus16': ['victus16_1.webp', 'victus16_2.webp'],
    'msikatana15': ['msikatana15_1.webp', 'msikatana15_2.webp'],
    # ... và nhiều mapping khác
}
```

### **Mapping theo từ khóa:**
```python
keywords = {
    'tuf': ['tuff15_1.webp', 'tuff15_2.webp'],
    'gaming': ['tuff15_1.webp', 'victus16_1.webp', 'legion5_1.webp'],
    'creator': ['creator16_1.webp', 'creator16_2.webp'],
    'xps': ['xps15_1.webp', 'xps15_2.webp'],
    # ... và nhiều từ khóa khác
}
```

## 📊 Kết quả mapping

| Laptop | Hình ảnh | Trạng thái |
|--------|----------|------------|
| ASUS TUF Gaming F15 | tuff15_1.webp | ✅ |
| HP Victus 16 | victus16_1.webp | ✅ |
| MSI Katana 15 | msikatana15_1.webp | ✅ |
| Lenovo Legion 5 | legion5_1.webp | ✅ |
| MSI Creator M16 | creator16_1.webp | ✅ |
| ASUS ProArt StudioBook | proartstudiobook_1.webp | ✅ |
| Dell XPS 15 | xps15_1.webp | ✅ |
| MacBook Pro 14 M3 | macbookpro14m3_1.webp | ✅ |
| Acer Swift Go 14 | acerswiftgo14_1.webp | ✅ |
| Lenovo ThinkPad X1 | thinkpadx1_1.webp | ✅ |
| Dell Precision 5570 | dellprecision5570_1.webp | ✅ |
| HP ZBook Studio | zbookstu_1.webp | ✅ |
| Acer Aspire 7 A715 | aspire7a715_1.webp | ✅ |
| MacBook Air 13 M2 | air13M2_1.webp | ✅ |
| ASUS VivoBook 15 | asusvivobook15_1.webp | ✅ |
| Lenovo IdeaPad 3 | ideapad3_1.webp | ✅ |
| Dell Inspiron 14 | Dellinspiron14_1.webp | ✅ |
| Lenovo IdeaPad 5 | ideapad5_1.webp | ✅ |
| HP Pavilion 14 | Pavilion14_1.webp | ✅ |
| Acer Aspire 3 | aspire3_1.webp | ✅ |
| ASUS E410 | asusE410_1.webp | ✅ |
| Lenovo IdeaPad 1 | lenovoIdeaPad_1.webp | ✅ |
| HP 15s | HP15s_1.webp | ✅ |
| Acer Aspire 1 | Aspire1_1.webp | ✅ |

## 🔧 Cách thêm hình ảnh mới

### **Bước 1: Thêm file hình ảnh**
```bash
# Copy file vào thư mục static/images/
cp your_image.webp static/images/
```

### **Bước 2: Cập nhật mapping (nếu cần)**
```python
# Trong update_images_auto.py, thêm vào mappings
'your_laptop_name': ['your_image.webp']
```

### **Bước 3: Chạy script cập nhật**
```bash
python update_images_auto.py
```

## 🎯 Tính năng nâng cao

### **Hỗ trợ nhiều hình ảnh:**
- Mỗi laptop có thể có nhiều hình ảnh
- Script sẽ chọn hình đầu tiên trong danh sách
- Có thể thêm hình 2, 3, 4... cho mỗi laptop

### **Định dạng hỗ trợ:**
- **WebP**: Hiệu suất tốt nhất, kích thước nhỏ
- **JPG/JPEG**: Tương thích rộng
- **PNG**: Chất lượng cao, hỗ trợ trong suốt

### **Tự động backup:**
- Script không xóa hình ảnh cũ
- Có thể rollback về trạng thái trước
- Lưu trữ an toàn

## 🚀 Tối ưu hóa

### **Kích thước hình ảnh:**
- **Khuyến nghị**: 400x250px
- **Định dạng**: WebP cho hiệu suất tốt nhất
- **Kích thước file**: < 500KB

### **Naming convention:**
```
brand_model_number.format
Ví dụ: tuff15_1.webp, victus16_2.webp
```

### **Performance:**
- Hình ảnh được serve từ static folder
- Không cần xử lý server-side
- Load nhanh trên web

## 🔍 Troubleshooting

### **Lỗi thường gặp:**

1. **Hình ảnh không hiển thị:**
   - Kiểm tra đường dẫn trong database
   - Đảm bảo file tồn tại trong static/images/
   - Kiểm tra quyền truy cập file

2. **Mapping không đúng:**
   - Kiểm tra tên file và tên laptop
   - Cập nhật mapping trong script
   - Chạy lại script

3. **File không được nhận diện:**
   - Kiểm tra định dạng file (.webp, .jpg, .png)
   - Đảm bảo tên file không có ký tự đặc biệt
   - Thử đổi tên file

### **Debug:**
```bash
# Kiểm tra file trong thư mục
ls static/images/

# Kiểm tra database
python check_images.py

# Chạy script với verbose
python update_images_auto.py
```

## 📈 Phát triển tiếp

### **Tính năng có thể thêm:**
- Upload hình ảnh qua web interface
- Tự động resize hình ảnh
- Hỗ trợ nhiều hình ảnh cho mỗi laptop
- Gallery view cho laptop
- Lazy loading cho performance

### **Cải thiện:**
- AI để tự động nhận diện laptop trong hình
- Compression tự động
- CDN integration
- Image optimization 