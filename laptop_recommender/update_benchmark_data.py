#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script cập nhật dữ liệu benchmark cho laptop
Sử dụng: python update_benchmark_data.py
"""

from app import create_app
from models import db, Laptop

def update_benchmark_data():
    """Cập nhật dữ liệu benchmark cho laptop"""
    app = create_app()
    with app.app_context():
        
        # Dữ liệu benchmark mẫu
        benchmark_data = {
            # ASUS TUF Gaming F15
            "ASUS TUF Gaming F15": {
                "battery_capacity": 90,
                "battery_life_office": 420,  # 7 giờ
                "battery_life_gaming": 180,  # 3 giờ
                "cpu_single_core_plugged": 2117,
                "cpu_multi_core_plugged": 6718,
                "cpu_single_core_battery": 1850,
                "cpu_multi_core_battery": 5800,
                "gpu_score_plugged": 8500,
                "gpu_score_battery": 6500
            },
            
            # HP Victus 16
            "HP Victus 16": {
                "battery_capacity": 83,
                "battery_life_office": 480,  # 8 giờ
                "battery_life_gaming": 210,  # 3.5 giờ
                "cpu_single_core_plugged": 2050,
                "cpu_multi_core_plugged": 7200,
                "cpu_single_core_battery": 1800,
                "cpu_multi_core_battery": 6200,
                "gpu_score_plugged": 9200,
                "gpu_score_battery": 7000
            },
            
            # MSI Katana 15
            "MSI Katana 15": {
                "battery_capacity": 76,
                "battery_life_office": 360,  # 6 giờ
                "battery_life_gaming": 150,  # 2.5 giờ
                "cpu_single_core_plugged": 1980,
                "cpu_multi_core_plugged": 6800,
                "cpu_single_core_battery": 1750,
                "cpu_multi_core_battery": 5900,
                "gpu_score_plugged": 7800,
                "gpu_score_battery": 5800
            },
            
            # Lenovo Legion 5
            "Lenovo Legion 5": {
                "battery_capacity": 80,
                "battery_life_office": 450,  # 7.5 giờ
                "battery_life_gaming": 200,  # 3.3 giờ
                "cpu_single_core_plugged": 2100,
                "cpu_multi_core_plugged": 7500,
                "cpu_single_core_battery": 1850,
                "cpu_multi_core_battery": 6500,
                "gpu_score_plugged": 9500,
                "gpu_score_battery": 7200
            },
            
            # MSI Creator M16
            "MSI Creator M16": {
                "battery_capacity": 99,
                "battery_life_office": 600,  # 10 giờ
                "battery_life_gaming": 240,  # 4 giờ
                "cpu_single_core_plugged": 2250,
                "cpu_multi_core_plugged": 8500,
                "cpu_single_core_battery": 2000,
                "cpu_multi_core_battery": 7500,
                "gpu_score_plugged": 12000,
                "gpu_score_battery": 9000
            },
            
            # ASUS ProArt StudioBook
            "ASUS ProArt StudioBook": {
                "battery_capacity": 92,
                "battery_life_office": 540,  # 9 giờ
                "battery_life_gaming": 180,  # 3 giờ
                "cpu_single_core_plugged": 2200,
                "cpu_multi_core_plugged": 8200,
                "cpu_single_core_battery": 1950,
                "cpu_multi_core_battery": 7200,
                "gpu_score_plugged": 11000,
                "gpu_score_battery": 8500
            },
            
            # Dell XPS 15
            "Dell XPS 15": {
                "battery_capacity": 86,
                "battery_life_office": 510,  # 8.5 giờ
                "battery_life_gaming": 180,  # 3 giờ
                "cpu_single_core_plugged": 2180,
                "cpu_multi_core_plugged": 8000,
                "cpu_single_core_battery": 1900,
                "cpu_multi_core_battery": 7000,
                "gpu_score_plugged": 10500,
                "gpu_score_battery": 8000
            },
            
            # MacBook Pro 14 M3
            "MacBook Pro 14 M3": {
                "battery_capacity": 72,
                "battery_life_office": 1200,  # 20 giờ
                "battery_life_gaming": 480,  # 8 giờ
                "cpu_single_core_plugged": 2400,
                "cpu_multi_core_plugged": 12000,
                "cpu_single_core_battery": 2350,
                "cpu_multi_core_battery": 11500,
                "gpu_score_plugged": 15000,
                "gpu_score_battery": 14000
            },
            
            # Acer Swift Go 14
            "Acer Swift Go 14": {
                "battery_capacity": 65,
                "battery_life_office": 480,  # 8 giờ
                "battery_life_gaming": 120,  # 2 giờ
                "cpu_single_core_plugged": 1800,
                "cpu_multi_core_plugged": 5500,
                "cpu_single_core_battery": 1600,
                "cpu_multi_core_battery": 4800,
                "gpu_score_plugged": 3500,
                "gpu_score_battery": 2800
            },
            
            # Lenovo ThinkPad X1
            "Lenovo ThinkPad X1": {
                "battery_capacity": 57,
                "battery_life_office": 540,  # 9 giờ
                "battery_life_gaming": 90,  # 1.5 giờ
                "cpu_single_core_plugged": 1900,
                "cpu_multi_core_plugged": 6000,
                "cpu_single_core_battery": 1700,
                "cpu_multi_core_battery": 5200,
                "gpu_score_plugged": 4000,
                "gpu_score_battery": 3200
            },
            
            # Dell Precision 5570
            "Dell Precision 5570": {
                "battery_capacity": 86,
                "battery_life_office": 480,  # 8 giờ
                "battery_life_gaming": 180,  # 3 giờ
                "cpu_single_core_plugged": 2100,
                "cpu_multi_core_plugged": 7800,
                "cpu_single_core_battery": 1850,
                "cpu_multi_core_battery": 6800,
                "gpu_score_plugged": 9500,
                "gpu_score_battery": 7200
            },
            
            # HP ZBook Studio
            "HP ZBook Studio": {
                "battery_capacity": 83,
                "battery_life_office": 450,  # 7.5 giờ
                "battery_life_gaming": 150,  # 2.5 giờ
                "cpu_single_core_plugged": 2050,
                "cpu_multi_core_plugged": 7500,
                "cpu_single_core_battery": 1800,
                "cpu_multi_core_battery": 6500,
                "gpu_score_plugged": 9000,
                "gpu_score_battery": 6800
            },
            
            # Acer Aspire 7 A715
            "Acer Aspire 7 A715": {
                "battery_capacity": 50,
                "battery_life_office": 300,  # 5 giờ
                "battery_life_gaming": 90,  # 1.5 giờ
                "cpu_single_core_plugged": 1600,
                "cpu_multi_core_plugged": 4800,
                "cpu_single_core_battery": 1400,
                "cpu_multi_core_battery": 4200,
                "gpu_score_plugged": 2800,
                "gpu_score_battery": 2200
            },
            
            # MacBook Air 13 M2
            "MacBook Air 13 M2": {
                "battery_capacity": 52,
                "battery_life_office": 900,  # 15 giờ
                "battery_life_gaming": 360,  # 6 giờ
                "cpu_single_core_plugged": 2200,
                "cpu_multi_core_plugged": 8500,
                "cpu_single_core_battery": 2150,
                "cpu_multi_core_battery": 8200,
                "gpu_score_plugged": 8000,
                "gpu_score_battery": 7500
            },
            
            # ASUS VivoBook 15
            "ASUS VivoBook 15": {
                "battery_capacity": 42,
                "battery_life_office": 360,  # 6 giờ
                "battery_life_gaming": 60,  # 1 giờ
                "cpu_single_core_plugged": 1400,
                "cpu_multi_core_plugged": 4200,
                "cpu_single_core_battery": 1200,
                "cpu_multi_core_battery": 3600,
                "gpu_score_plugged": 2000,
                "gpu_score_battery": 1500
            },
            
            # Lenovo IdeaPad 3
            "Lenovo IdeaPad 3": {
                "battery_capacity": 45,
                "battery_life_office": 330,  # 5.5 giờ
                "battery_life_gaming": 75,  # 1.25 giờ
                "cpu_single_core_plugged": 1350,
                "cpu_multi_core_plugged": 4000,
                "cpu_single_core_battery": 1150,
                "cpu_multi_core_battery": 3500,
                "gpu_score_plugged": 1800,
                "gpu_score_battery": 1300
            },
            
            # Dell Inspiron 14
            "Dell Inspiron 14": {
                "battery_capacity": 54,
                "battery_life_office": 420,  # 7 giờ
                "battery_life_gaming": 90,  # 1.5 giờ
                "cpu_single_core_plugged": 1500,
                "cpu_multi_core_plugged": 4500,
                "cpu_single_core_battery": 1300,
                "cpu_multi_core_battery": 3900,
                "gpu_score_plugged": 2200,
                "gpu_score_battery": 1700
            },
            
            # Lenovo IdeaPad 5
            "Lenovo IdeaPad 5": {
                "battery_capacity": 57,
                "battery_life_office": 480,  # 8 giờ
                "battery_life_gaming": 120,  # 2 giờ
                "cpu_single_core_plugged": 1600,
                "cpu_multi_core_plugged": 4800,
                "cpu_single_core_battery": 1400,
                "cpu_multi_core_battery": 4200,
                "gpu_score_plugged": 2500,
                "gpu_score_battery": 2000
            },
            
            # HP Pavilion 14
            "HP Pavilion 14": {
                "battery_capacity": 43,
                "battery_life_office": 390,  # 6.5 giờ
                "battery_life_gaming": 75,  # 1.25 giờ
                "cpu_single_core_plugged": 1450,
                "cpu_multi_core_plugged": 4300,
                "cpu_single_core_battery": 1250,
                "cpu_multi_core_battery": 3700,
                "gpu_score_plugged": 2100,
                "gpu_score_battery": 1600
            },
            
            # Acer Aspire 3
            "Acer Aspire 3": {
                "battery_capacity": 36,
                "battery_life_office": 300,  # 5 giờ
                "battery_life_gaming": 60,  # 1 giờ
                "cpu_single_core_plugged": 1200,
                "cpu_multi_core_plugged": 3500,
                "cpu_single_core_battery": 1000,
                "cpu_multi_core_battery": 3000,
                "gpu_score_plugged": 1500,
                "gpu_score_battery": 1100
            },
            
            # ASUS E410
            "ASUS E410": {
                "battery_capacity": 42,
                "battery_life_office": 360,  # 6 giờ
                "battery_life_gaming": 45,  # 0.75 giờ
                "cpu_single_core_plugged": 1100,
                "cpu_multi_core_plugged": 3200,
                "cpu_single_core_battery": 900,
                "cpu_multi_core_battery": 2800,
                "gpu_score_plugged": 1200,
                "gpu_score_battery": 800
            },
            
            # Lenovo IdeaPad 1
            "Lenovo IdeaPad 1": {
                "battery_capacity": 45,
                "battery_life_office": 420,  # 7 giờ
                "battery_life_gaming": 30,  # 0.5 giờ
                "cpu_single_core_plugged": 1000,
                "cpu_multi_core_plugged": 2800,
                "cpu_single_core_battery": 800,
                "cpu_multi_core_battery": 2400,
                "gpu_score_plugged": 800,
                "gpu_score_battery": 500
            },
            
            # HP 15s
            "HP 15s": {
                "battery_capacity": 41,
                "battery_life_office": 390,  # 6.5 giờ
                "battery_life_gaming": 60,  # 1 giờ
                "cpu_single_core_plugged": 1150,
                "cpu_multi_core_plugged": 3300,
                "cpu_single_core_battery": 950,
                "cpu_multi_core_battery": 2900,
                "gpu_score_plugged": 1300,
                "gpu_score_battery": 900
            },
            
            # Acer Aspire 1
            "Acer Aspire 1": {
                "battery_capacity": 36,
                "battery_life_office": 330,  # 5.5 giờ
                "battery_life_gaming": 30,  # 0.5 giờ
                "cpu_single_core_plugged": 900,
                "cpu_multi_core_plugged": 2500,
                "cpu_single_core_battery": 700,
                "cpu_multi_core_battery": 2100,
                "gpu_score_plugged": 600,
                "gpu_score_battery": 400
            }
        }
        
        print("🔄 Đang cập nhật dữ liệu benchmark...")
        updated_count = 0
        
        for laptop_name, data in benchmark_data.items():
            laptop = Laptop.query.filter_by(name=laptop_name).first()
            if laptop:
                # Cập nhật dữ liệu
                laptop.battery_capacity = data["battery_capacity"]
                laptop.battery_life_office = data["battery_life_office"]
                laptop.battery_life_gaming = data["battery_life_gaming"]
                laptop.cpu_single_core_plugged = data["cpu_single_core_plugged"]
                laptop.cpu_multi_core_plugged = data["cpu_multi_core_plugged"]
                laptop.cpu_single_core_battery = data["cpu_single_core_battery"]
                laptop.cpu_multi_core_battery = data["cpu_multi_core_battery"]
                laptop.gpu_score_plugged = data["gpu_score_plugged"]
                laptop.gpu_score_battery = data["gpu_score_battery"]
                
                updated_count += 1
                print(f"✅ {laptop_name}")
            else:
                print(f"❌ Không tìm thấy: {laptop_name}")
        
        # Lưu thay đổi
        db.session.commit()
        
        print(f"\n🎉 Hoàn thành! Đã cập nhật {updated_count} laptop")
        print("\n📊 Thống kê dữ liệu:")
        
        # Thống kê
        total = Laptop.query.count()
        with_battery = Laptop.query.filter(Laptop.battery_capacity.isnot(None)).count()
        with_cpu_scores = Laptop.query.filter(Laptop.cpu_single_core_plugged.isnot(None)).count()
        with_gpu_scores = Laptop.query.filter(Laptop.gpu_score_plugged.isnot(None)).count()
        
        print(f"   🔋 Có dữ liệu pin: {with_battery}/{total}")
        print(f"   🖥️  Có điểm CPU: {with_cpu_scores}/{total}")
        print(f"   🎮 Có điểm GPU: {with_gpu_scores}/{total}")

if __name__ == "__main__":
    update_benchmark_data() 