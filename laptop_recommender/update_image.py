from app import create_app
from models import db, Laptop

def update_laptop_image():
    app = create_app()
    with app.app_context():
        # Tìm laptop Acer Aspire 3
        laptop = Laptop.query.filter(Laptop.name.like('%Acer Aspire 3%')).first()
        
        if laptop:
            # Cập nhật đường dẫn hình ảnh
            laptop.image_url = '/static/images/aceraspire3.jpg'
            db.session.commit()
            print(f"Đã cập nhật hình ảnh cho {laptop.name}")
            print(f"Đường dẫn: {laptop.image_url}")
        else:
            print("Không tìm thấy laptop Acer Aspire 3")

if __name__ == "__main__":
    update_laptop_image() 