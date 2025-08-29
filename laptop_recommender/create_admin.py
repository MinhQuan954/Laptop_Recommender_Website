#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tạo admin user
Sử dụng: python create_admin.py
"""

from app import create_app
from models import db, User

def create_admin():
    """Tạo admin user"""
    app = create_app()
    with app.app_context():
        
        # Kiểm tra xem đã có admin chưa
        admin = User.query.filter_by(role='admin').first()
        if admin:
            print(f"⚠️  Đã có admin: {admin.username}")
            return
        
        # Tạo admin mới
        admin = User(
            username='admin',
            email='admin@laptop.com',
            role='admin'
        )
        admin.set_password('admin123')
        
        try:
            db.session.add(admin)
            db.session.commit()
            print("✅ Đã tạo admin thành công!")
            print("📋 Thông tin đăng nhập:")
            print("   👤 Username: admin")
            print("   🔑 Password: admin123")
            print("   📧 Email: admin@laptop.com")
            print("\n🔗 Truy cập: http://localhost:5000/admin")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Lỗi khi tạo admin: {e}")

def update_existing_user_to_admin():
    """Cập nhật user hiện có thành admin"""
    app = create_app()
    with app.app_context():
        
        username = input("Nhập username muốn cấp quyền admin: ").strip()
        if not username:
            print("❌ Username không được để trống!")
            return
        
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"❌ Không tìm thấy user: {username}")
            return
        
        user.role = 'admin'
        try:
            db.session.commit()
            print(f"✅ Đã cấp quyền admin cho user: {username}")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Lỗi khi cập nhật: {e}")

def main():
    print("🛠️  QUẢN LÝ ADMIN USER")
    print("=" * 40)
    print("1. Tạo admin mới")
    print("2. Cấp quyền admin cho user hiện có")
    print("3. Thoát")
    
    choice = input("\nChọn tùy chọn (1-3): ").strip()
    
    if choice == '1':
        create_admin()
    elif choice == '2':
        update_existing_user_to_admin()
    elif choice == '3':
        print("👋 Tạm biệt!")
    else:
        print("❌ Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main() 