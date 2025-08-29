#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script thêm hình ảnh cho laptop
Sử dụng: python them_hinh_anh.py
"""

from app import create_app
from models import db, Laptop
import os

def them_hinh_anh():
    app = create_app()
    with app.app_context():
        print("=== HƯỚNG DẪN THÊM HÌNH ẢNH ===")
        print("1. Copy file hình ảnh vào thư mục static/images/")
        print("2. Nhập tên laptop và tên file hình ảnh")
        print("3. Hệ thống sẽ tự động cập nhật database")
        print()
        
        # Hiển thị danh sách laptop hiện tại
        laptops = Laptop.query.all()
        print("Danh sách laptop hiện tại:")
        for i, laptop in enumerate(laptops, 1):
            status = "✓" if laptop.image_url and "placeholder" not in laptop.image_url else "✗"
            print(f"{i:2d}. {status} {laptop.name} ({laptop.brand})")
        
        print("\n" + "="*50)
        
        # Nhập thông tin
        laptop_name = input("Nhập tên laptop (hoặc một phần tên): ").strip()
        image_filename = input("Nhập tên file hình ảnh (ví dụ: asus_tuf.jpg): ").strip()
        
        if not laptop_name or not image_filename:
            print("❌ Vui lòng nhập đầy đủ thông tin!")
            return
        
        # Kiểm tra file hình ảnh có tồn tại không
        image_path = os.path.join('static', 'images', image_filename)
        if not os.path.exists(image_path):
            print(f"❌ Không tìm thấy file: {image_path}")
            print("Hãy đảm bảo file đã được copy vào thư mục static/images/")
            return
        
        # Tìm laptop
        laptop = Laptop.query.filter(Laptop.name.like(f'%{laptop_name}%')).first()
        
        if not laptop:
            print(f"❌ Không tìm thấy laptop có tên chứa: {laptop_name}")
            return
        
        # Cập nhật hình ảnh
        laptop.image_url = f'/static/images/{image_filename}'
        db.session.commit()
        
        print(f"✅ Đã cập nhật thành công!")
        print(f"   Laptop: {laptop.name}")
        print(f"   Hình ảnh: {laptop.image_url}")
        print(f"   File: {image_path}")

def xem_hinh_anh():
    """Xem danh sách hình ảnh hiện tại"""
    app = create_app()
    with app.app_context():
        laptops = Laptop.query.all()
        
        print("=== DANH SÁCH HÌNH ẢNH HIỆN TẠI ===")
        for laptop in laptops:
            if laptop.image_url:
                if "placeholder" in laptop.image_url:
                    status = "🖼️  Placeholder"
                else:
                    status = "✅ Hình thật"
                print(f"{status} | {laptop.name}")
                print(f"        URL: {laptop.image_url}")
            else:
                print(f"❌ Chưa có | {laptop.name}")
            print()

def main():
    while True:
        print("\n=== MENU THÊM HÌNH ẢNH ===")
        print("1. Thêm hình ảnh mới")
        print("2. Xem danh sách hình ảnh hiện tại")
        print("3. Thoát")
        
        choice = input("\nChọn tùy chọn (1-3): ").strip()
        
        if choice == '1':
            them_hinh_anh()
        elif choice == '2':
            xem_hinh_anh()
        elif choice == '3':
            print("Tạm biệt!")
            break
        else:
            print("❌ Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main() 