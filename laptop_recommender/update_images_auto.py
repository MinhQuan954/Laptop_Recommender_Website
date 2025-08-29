#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tự động cập nhật hình ảnh theo tên máy
Sử dụng: python update_images_auto.py
"""

from app import create_app
from models import db, Laptop
import os
import re

def normalize_name(name):
    """Chuẩn hóa tên để so sánh"""
    # Chuyển về lowercase và loại bỏ ký tự đặc biệt
    name = name.lower()
    name = re.sub(r'[^a-z0-9]', '', name)
    return name

def find_best_match(laptop_name, image_files):
    """Tìm hình ảnh phù hợp nhất cho laptop"""
    laptop_normalized = normalize_name(laptop_name)
    
    # Tạo mapping từ tên laptop đến tên file hình ảnh
    mappings = {
        # ASUS
        'asustufgamingf15': ['tuff15_1.webp', 'tuff15_2.webp'],
        'asusproartstudiobook': ['proartstudiobook_1.webp', 'proartstudiobook_2.webp'],
        'asusvivobook15': ['asusvivobook15_1.webp', 'asusvivobook15_2.webp'],
        'asuse410': ['asusE410_1.webp', 'asusE410_2.webp'],
        
        # HP
        'hpvictus16': ['victus16_1.webp', 'victus16_2.webp'],
        'hpzbookstudio': ['zbookstu_1.webp', 'zbookstu_2.webp'],
        'hppavilion14': ['Pavilion14_1.webp', 'Pavilion14_2.webp'],
        'hp15s': ['HP15s_1.webp', 'HP15s_2.webp'],
        
        # MSI
        'msikatana15': ['msikatana15_1.webp', 'msikatana15_2.webp'],
        'msicreatorm16': ['creator16_1.webp', 'creator16_2.webp'],
        
        # Lenovo
        'lenovolegion5': ['legion5_1.webp', 'legion5_2.webp'],
        'lenovothinkpadx1': ['thinkpadx1_1.webp', 'thinkpadx1_2.webp'],
        'lenovoideapad3': ['ideapad3_1.webp', 'ideapad3_2.webp'],
        'lenovoideapad5': ['ideapad5_1.webp', 'ideapad5_2.webp'],
        'lenovoideapad1': ['lenovoIdeaPad_1.webp', 'lenovoIdeaPad_2.webp'],
        
        # Dell
        'dellxps15': ['xps15_1.webp', 'xps15_2.webp'],
        'dellprecision5570': ['dellprecision5570_1.webp', 'dellprecision5570_2.webp'],
        'dellinspiron14': ['Dellinspiron14_1.webp', 'Dellinspiron14_2.webp'],
        
        # Apple
        'macbookpro14m3': ['macbookpro14m3_1.webp', 'macbookpro14m3_2.webp'],
        'macbookair13m2': ['air13M2_1.webp', 'air13M2_2.webp'],
        
        # Acer
        'acerswiftgo14': ['acerswiftgo14_1.webp', 'acerswiftgo14_2.webp'],
        'aceraspire7a715': ['aspire7a715_1.webp', 'aspire7a715_2.webp'],
        'aceraspire3': ['aspire3_1.webp', 'aspire3_2.webp', 'aceraspire3.webp'],
        'aceraspire1': ['Aspire1_1.webp', 'Aspire1_2.webp', 'Aspire1_3.webp'],
    }
    
    # Tìm match chính xác
    for key, images in mappings.items():
        if key in laptop_normalized or laptop_normalized in key:
            # Kiểm tra file nào tồn tại
            for img in images:
                if img in image_files:
                    return img
    
    # Tìm match theo từ khóa
    keywords = {
        'tuf': ['tuff15_1.webp', 'tuff15_2.webp'],
        'gaming': ['tuff15_1.webp', 'victus16_1.webp', 'legion5_1.webp'],
        'creator': ['creator16_1.webp', 'creator16_2.webp'],
        'proart': ['proartstudiobook_1.webp', 'proartstudiobook_2.webp'],
        'xps': ['xps15_1.webp', 'xps15_2.webp'],
        'precision': ['dellprecision5570_1.webp', 'dellprecision5570_2.webp'],
        'thinkpad': ['thinkpadx1_1.webp', 'thinkpadx1_2.webp'],
        'swift': ['acerswiftgo14_1.webp', 'acerswiftgo14_2.webp'],
        'aspire': ['aspire3_1.webp', 'aspire7a715_1.webp'],
        'vivobook': ['asusvivobook15_1.webp', 'asusvivobook15_2.webp'],
        'ideapad': ['ideapad3_1.webp', 'ideapad5_1.webp'],
        'pavilion': ['Pavilion14_1.webp', 'Pavilion14_2.webp'],
        'victus': ['victus16_1.webp', 'victus16_2.webp'],
        'legion': ['legion5_1.webp', 'legion5_2.webp'],
        'zbook': ['zbookstu_1.webp', 'zbookstu_2.webp'],
        'macbook': ['macbookpro14m3_1.webp', 'air13M2_1.webp'],
        'inspiron': ['Dellinspiron14_1.webp', 'Dellinspiron14_2.webp'],
    }
    
    for keyword, images in keywords.items():
        if keyword in laptop_normalized:
            for img in images:
                if img in image_files:
                    return img
    
    return None

def update_all_images():
    """Cập nhật hình ảnh cho tất cả laptop"""
    app = create_app()
    with app.app_context():
        # Lấy danh sách file hình ảnh
        image_dir = 'static/images'
        image_files = [f for f in os.listdir(image_dir) if f.endswith(('.webp', '.jpg', '.png', '.jpeg'))]
        
        print(f"📁 Tìm thấy {len(image_files)} file hình ảnh")
        print("🔄 Đang cập nhật hình ảnh cho laptop...")
        print("=" * 60)
        
        # Lấy tất cả laptop
        laptops = Laptop.query.all()
        updated_count = 0
        
        for laptop in laptops:
            # Tìm hình ảnh phù hợp
            best_image = find_best_match(laptop.name, image_files)
            
            if best_image:
                # Cập nhật đường dẫn hình ảnh
                laptop.image_url = f'/static/images/{best_image}'
                updated_count += 1
                print(f"✅ {laptop.name}")
                print(f"   📸 {best_image}")
            else:
                # Giữ nguyên placeholder nếu không tìm thấy
                if not laptop.image_url or 'placeholder' in laptop.image_url:
                    print(f"❌ {laptop.name} - Không tìm thấy hình ảnh phù hợp")
                else:
                    print(f"⚠️  {laptop.name} - Giữ nguyên hình ảnh hiện tại")
        
        # Lưu thay đổi
        db.session.commit()
        
        print("=" * 60)
        print(f"🎉 Hoàn thành! Đã cập nhật {updated_count}/{len(laptops)} laptop")
        
        # Hiển thị thống kê
        print("\n📊 Thống kê:")
        laptops_with_images = Laptop.query.filter(Laptop.image_url.like('%webp%')).count()
        laptops_with_placeholders = Laptop.query.filter(Laptop.image_url.like('%placeholder%')).count()
        laptops_without_images = len(laptops) - laptops_with_images - laptops_with_placeholders
        
        print(f"   🖼️  Có hình thật: {laptops_with_images}")
        print(f"   🎨 Có placeholder: {laptops_with_placeholders}")
        print(f"   ❌ Không có hình: {laptops_without_images}")

def show_image_mapping():
    """Hiển thị mapping hình ảnh hiện tại"""
    app = create_app()
    with app.app_context():
        laptops = Laptop.query.all()
        
        print("📋 MAPPING HÌNH ẢNH HIỆN TẠI:")
        print("=" * 80)
        
        for laptop in laptops:
            status = "✅" if laptop.image_url and "placeholder" not in laptop.image_url else "❌"
            image_name = laptop.image_url.split('/')[-1] if laptop.image_url else "Không có"
            print(f"{status} {laptop.name}")
            print(f"   📸 {image_name}")
            print()

def main():
    while True:
        print("\n🖼️  QUẢN LÝ HÌNH ẢNH LAPTOP")
        print("=" * 40)
        print("1. Tự động cập nhật hình ảnh")
        print("2. Xem mapping hiện tại")
        print("3. Thoát")
        
        choice = input("\nChọn tùy chọn (1-3): ").strip()
        
        if choice == '1':
            update_all_images()
        elif choice == '2':
            show_image_mapping()
        elif choice == '3':
            print("👋 Tạm biệt!")
            break
        else:
            print("❌ Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main() 