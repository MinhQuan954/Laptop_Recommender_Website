from app import create_app
from models import db, Laptop

def add_images_to_laptops():
    app = create_app()
    with app.app_context():
        laptops = Laptop.query.all()
        
        for laptop in laptops:
            if not laptop.image_url or laptop.image_url == '':
                # Tạo tên file hình ảnh dựa trên tên laptop
                brand_lower = laptop.brand.lower()
                name_lower = laptop.name.lower().replace(' ', '').replace('-', '')
                
                # Nếu có hình ảnh thực tế, sử dụng nó
                if brand_lower == 'acer' and 'aspire3' in name_lower:
                    laptop.image_url = '/static/images/aceraspire3.jpg'
                else:
                    # Sử dụng placeholder với thông tin laptop
                    laptop.image_url = f'https://via.placeholder.com/400x250/007bff/ffffff?text={laptop.brand}+{laptop.name.split()[0]}'
                
                print(f"Đã cập nhật hình ảnh cho {laptop.name}: {laptop.image_url}")
        
        db.session.commit()
        print(f"Đã cập nhật hình ảnh cho {len(laptops)} laptop")

if __name__ == "__main__":
    add_images_to_laptops() 