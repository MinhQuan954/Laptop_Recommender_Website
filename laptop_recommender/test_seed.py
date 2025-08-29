from app import create_app
from models import db, Laptop

def main():
    app = create_app()
    with app.app_context():
        # Xóa dữ liệu cũ
        db.drop_all()
        db.create_all()
        
        # Thêm dữ liệu mẫu
        laptops = [
            Laptop(name="ASUS TUF Gaming F15", brand="ASUS", cpu="Core i5-11400H", ram_gb=16, gpu="RTX 3050", storage="512GB SSD", screen="15.6 FHD 144Hz", price=21000000, category="gaming"),
            Laptop(name="HP Victus 16", brand="HP", cpu="Ryzen 7 7840HS", ram_gb=16, gpu="RTX 4060", storage="512GB SSD", screen="16.1 FHD 144Hz", price=36000000, category="gaming"),
            Laptop(name="MSI Creator M16", brand="MSI", cpu="Core i7-12650H", ram_gb=16, gpu="RTX 4050", storage="1TB SSD", screen="16 2.5K 120Hz", price=35000000, category="design"),
            Laptop(name="Dell Inspiron 14", brand="Dell", cpu="Core i5-1235U", ram_gb=16, gpu="Iris Xe", storage="512GB SSD", screen="14 FHD", price=18500000, category="office"),
            Laptop(name="Acer Aspire 3", brand="Acer", cpu="Ryzen 3 7320U", ram_gb=8, gpu="Radeon Graphics", storage="256GB SSD", screen="15.6 FHD", price=8500000, category="office"),
        ]
        
        for laptop in laptops:
            db.session.add(laptop)
        
        db.session.commit()
        print(f"Đã thêm {len(laptops)} laptop thành công!")

if __name__ == "__main__":
    main() 