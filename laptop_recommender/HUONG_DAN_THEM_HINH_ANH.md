# Hướng dẫn thêm hình ảnh cho laptop

## Cấu trúc thư mục
```
laptop_recommender/
├── static/
│   └── images/
│       ├── aceraspire3.jpg
│       ├── asus_tuf_gaming.jpg
│       ├── hp_victus.jpg
│       └── ...
├── app.py
├── models.py
└── ...
```

## Cách thêm hình ảnh mới

### Bước 1: Đặt file hình ảnh vào thư mục static/images
- Copy file hình ảnh vào thư mục `static/images/`
- Đặt tên file theo format: `brand_model.jpg` (ví dụ: `asus_tuf_gaming.jpg`)

### Bước 2: Cập nhật database
Chạy script sau để cập nhật đường dẫn hình ảnh:

```python
from app import create_app
from models import db, Laptop

def update_laptop_image(laptop_name, image_filename):
    app = create_app()
    with app.app_context():
        laptop = Laptop.query.filter(Laptop.name.like(f'%{laptop_name}%')).first()
        
        if laptop:
            laptop.image_url = f'/static/images/{image_filename}'
            db.session.commit()
            print(f"Đã cập nhật hình ảnh cho {laptop.name}")
        else:
            print(f"Không tìm thấy laptop: {laptop_name}")

# Ví dụ:
update_laptop_image('ASUS TUF Gaming', 'asus_tuf_gaming.jpg')
update_laptop_image('HP Victus', 'hp_victus.jpg')
```

### Bước 3: Kiểm tra
- Truy cập trang web và xem hình ảnh đã hiển thị chưa
- URL hình ảnh sẽ là: `http://localhost:5000/static/images/ten_file.jpg`

## Lưu ý quan trọng

1. **Định dạng file**: Hỗ trợ .jpg, .png, .gif, .webp
2. **Kích thước**: Khuyến nghị 400x250px để hiển thị đẹp
3. **Tên file**: Không dùng dấu cách, thay bằng dấu gạch dưới (_)
4. **Đường dẫn**: Luôn bắt đầu bằng `/static/images/`

## Ví dụ thực tế

### Thêm hình ảnh cho ASUS TUF Gaming F15:
1. Copy file `asus_tuf_gaming_f15.jpg` vào `static/images/`
2. Chạy script:
```python
update_laptop_image('ASUS TUF Gaming F15', 'asus_tuf_gaming_f15.jpg')
```

### Thêm hình ảnh cho HP Victus 16:
1. Copy file `hp_victus_16.jpg` vào `static/images/`
2. Chạy script:
```python
update_laptop_image('HP Victus 16', 'hp_victus_16.jpg')
```

## Script tự động cập nhật tất cả

Nếu bạn có nhiều hình ảnh, có thể sử dụng script sau:

```python
from app import create_app
from models import db, Laptop
import os

def update_all_images():
    app = create_app()
    with app.app_context():
        # Lấy danh sách file hình ảnh
        image_dir = 'static/images'
        image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png', '.gif'))]
        
        for image_file in image_files:
            # Tạo tên laptop từ tên file
            name_parts = image_file.replace('.jpg', '').replace('.png', '').split('_')
            brand = name_parts[0].upper()
            
            # Tìm laptop tương ứng
            laptop = Laptop.query.filter(
                Laptop.brand.like(f'%{brand}%'),
                Laptop.name.like(f'%{" ".join(name_parts[1:]).upper()}%')
            ).first()
            
            if laptop:
                laptop.image_url = f'/static/images/{image_file}'
                print(f"Đã cập nhật {laptop.name} với {image_file}")
        
        db.session.commit()

update_all_images()
```

## Xử lý lỗi thường gặp

### Lỗi 1: Hình ảnh không hiển thị
- Kiểm tra file có tồn tại trong `static/images/` không
- Kiểm tra đường dẫn trong database có đúng không
- Kiểm tra tên file có chứa ký tự đặc biệt không

### Lỗi 2: Hình ảnh bị lỗi
- Kiểm tra định dạng file có được hỗ trợ không
- Thử đổi tên file thành tiếng Anh, không dấu

### Lỗi 3: Flask không phục vụ file tĩnh
- Đảm bảo đã cấu hình `static_folder='static'` trong `app.py`
- Restart server sau khi thêm file mới 