from app import create_app
from models import db, Laptop

app = create_app()
SAMPLE = [
    # Gaming laptops
    dict(name="ASUS TUF Gaming F15", brand="ASUS", cpu="Core i5-11400H", ram_gb=16, gpu="RTX 3050", storage="512GB SSD", screen="15.6 FHD 144Hz", price=21000000, category="gaming", image_url=""),
    dict(name="HP Victus 16", brand="HP", cpu="Ryzen 7 7840HS", ram_gb=16, gpu="RTX 4060", storage="512GB SSD", screen="16.1 FHD 144Hz", price=36000000, category="gaming", image_url=""),
    dict(name="MSI Katana 15", brand="MSI", cpu="Core i7-13620H", ram_gb=16, gpu="RTX 4070", storage="1TB SSD", screen="15.6 FHD 144Hz", price=42000000, category="gaming", image_url=""),
    dict(name="Lenovo Legion 5", brand="Lenovo", cpu="Ryzen 5 7640H", ram_gb=16, gpu="RTX 4050", storage="512GB SSD", screen="15.6 FHD 165Hz", price=28000000, category="gaming", image_url=""),
    
    # Design laptops
    dict(name="MSI Creator M16", brand="MSI", cpu="Core i7-12650H", ram_gb=16, gpu="RTX 4050", storage="1TB SSD", screen="16 2.5K 120Hz", price=35000000, category="design", image_url=""),
    dict(name="ASUS ProArt StudioBook", brand="ASUS", cpu="Core i7-13700H", ram_gb=32, gpu="RTX 4060", storage="1TB SSD", screen="16 2.5K 120Hz", price=45000000, category="design", image_url=""),
    dict(name="Dell XPS 15", brand="Dell", cpu="Core i7-13700H", ram_gb=16, gpu="RTX 4050", storage="512GB SSD", screen="15.6 3.5K OLED", price=48000000, category="design", image_url=""),
    dict(name="MacBook Pro 14 M3", brand="Apple", cpu="Apple M3", ram_gb=16, gpu="Integrated", storage="512GB SSD", screen="14.2 Liquid Retina", price=52000000, category="design", image_url=""),
    
    # Development laptops
    dict(name="Acer Swift Go 14", brand="Acer", cpu="Intel Core Ultra 5", ram_gb=16, gpu="Arc iGPU", storage="512GB SSD", screen="14 OLED 2.8K", price=28000000, category="dev", image_url=""),
    dict(name="Lenovo ThinkPad X1", brand="Lenovo", cpu="Core i7-1355U", ram_gb=16, gpu="Iris Xe", storage="512GB SSD", screen="14 2.2K", price=32000000, category="dev", image_url=""),
    dict(name="Dell Precision 5570", brand="Dell", cpu="Core i7-12700H", ram_gb=32, gpu="RTX A1000", storage="1TB SSD", screen="15.6 FHD", price=38000000, category="dev", image_url=""),
    dict(name="HP ZBook Studio", brand="HP", cpu="Core i7-13700H", ram_gb=16, gpu="RTX A2000", storage="512GB SSD", screen="15.6 4K", price=42000000, category="dev", image_url=""),
    
    # Student laptops
    dict(name="Acer Aspire 7 A715", brand="Acer", cpu="Ryzen 5 5500U", ram_gb=8, gpu="GTX 1650", storage="512GB SSD", screen="15.6 FHD 60Hz", price=14500000, category="student", image_url=""),
    dict(name="MacBook Air 13 M2", brand="Apple", cpu="Apple M2", ram_gb=8, gpu="Integrated", storage="256GB SSD", screen="13.6 60Hz", price=26000000, category="student", image_url=""),
    dict(name="ASUS VivoBook 15", brand="ASUS", cpu="Core i5-1235U", ram_gb=8, gpu="Iris Xe", storage="256GB SSD", screen="15.6 FHD", price=12000000, category="student", image_url=""),
    dict(name="Lenovo IdeaPad 3", brand="Lenovo", cpu="Ryzen 5 7520U", ram_gb=8, gpu="Radeon Graphics", storage="256GB SSD", screen="15.6 FHD", price=11000000, category="student", image_url=""),
    
    # Office laptops
    dict(name="Dell Inspiron 14", brand="Dell", cpu="Core i5-1235U", ram_gb=16, gpu="Iris Xe", storage="512GB SSD", screen="14 FHD", price=18500000, category="office", image_url=""),
    dict(name="Lenovo IdeaPad 5", brand="Lenovo", cpu="Ryzen 5 7530U", ram_gb=16, gpu="Radeon", storage="512GB SSD", screen="15.6 FHD", price=17900000, category="office", image_url=""),
    dict(name="HP Pavilion 14", brand="HP", cpu="Core i5-1335U", ram_gb=8, gpu="Iris Xe", storage="256GB SSD", screen="14 FHD", price=15000000, category="office", image_url=""),
    dict(name="Acer Aspire 3", brand="Acer", cpu="Ryzen 3 7320U", ram_gb=8, gpu="Radeon Graphics", storage="256GB SSD", screen="15.6 FHD", price=8500000, category="office", image_url="aceraspire3.jpg"),
    
    # Budget options
    dict(name="ASUS E410", brand="ASUS", cpu="Celeron N4020", ram_gb=4, gpu="Intel UHD", storage="128GB eMMC", screen="14 FHD", price=6500000, category="office", image_url=""),
    dict(name="Lenovo IdeaPad 1", brand="Lenovo", cpu="Athlon Silver 3050U", ram_gb=4, gpu="Radeon Graphics", storage="128GB SSD", screen="14 FHD", price=7000000, category="student", image_url=""),
    dict(name="HP 15s", brand="HP", cpu="Core i3-1215U", ram_gb=8, gpu="Intel UHD", storage="256GB SSD", screen="15.6 FHD", price=9500000, category="office", image_url=""),
    dict(name="Acer Aspire 1", brand="Acer", cpu="Celeron N4500", ram_gb=4, gpu="Intel UHD", storage="128GB eMMC", screen="15.6 FHD", price=6000000, category="office", image_url="")
]

with app.app_context():
    db.drop_all()
    db.create_all()
    for row in SAMPLE:
        db.session.add(Laptop(**row))
    db.session.commit()
    print(f"Seeded {len(SAMPLE)} laptops.")
