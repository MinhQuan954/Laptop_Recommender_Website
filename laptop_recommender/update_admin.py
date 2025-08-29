#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script cập nhật user hiện có thành admin
Sử dụng: python update_admin.py
"""

from app import create_app
from models import db, User

def update_admin():
    """Cập nhật user hiện có thành admin"""
    app = create_app()
    with app.app_context():
        
        # Lấy user đầu tiên và cập nhật thành admin
        user = User.query.first()
        if user:
            user.role = 'admin'
            try:
                db.session.commit()
                print(f"✅ Đã cấp quyền admin cho user: {user.username}")
                print(f"📧 Email: {user.email}")
                print("\n🔗 Truy cập: http://localhost:5000/admin")
            except Exception as e:
                db.session.rollback()
                print(f"❌ Lỗi khi cập nhật: {e}")
        else:
            print("❌ Không tìm thấy user nào!")

if __name__ == "__main__":
    update_admin() 