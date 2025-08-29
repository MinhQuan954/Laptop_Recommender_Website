#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script migration để thêm cột role cho user
Sử dụng: python migrate_admin.py
"""

from app import create_app
from models import db
import sqlite3
import os

def migrate_admin():
    """Migration để thêm cột role cho user"""
    app = create_app()
    
    with app.app_context():
        # Kiểm tra xem database có tồn tại không
        if not os.path.exists('app.db'):
            print("❌ Database không tồn tại. Tạo database mới...")
            db.create_all()
            print("✅ Đã tạo database mới")
            return
        
        # Kết nối trực tiếp đến SQLite để thêm cột
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        
        print("🔄 Đang migration database cho admin...")
        
        # Kiểm tra xem bảng users có tồn tại không
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("❌ Bảng users không tồn tại. Tạo bảng mới...")
            db.create_all()
            print("✅ Đã tạo bảng mới")
            conn.close()
            return
        
        # Lấy danh sách cột hiện tại
        cursor.execute("PRAGMA table_info(users)")
        existing_columns = [column[1] for column in cursor.fetchall()]
        
        # Thêm các cột mới nếu chưa tồn tại
        new_columns = [
            ('role', 'VARCHAR(20) DEFAULT "user"'),
            ('created_at', 'DATETIME')
        ]
        
        added_columns = 0
        for column_name, column_type in new_columns:
            if column_name not in existing_columns:
                try:
                    cursor.execute(f"ALTER TABLE users ADD COLUMN {column_name} {column_type}")
                    print(f"✅ Đã thêm cột: {column_name}")
                    added_columns += 1
                except sqlite3.OperationalError as e:
                    print(f"⚠️  Cột {column_name} đã tồn tại hoặc có lỗi: {e}")
            else:
                print(f"ℹ️  Cột {column_name} đã tồn tại")
        
        # Commit thay đổi
        conn.commit()
        conn.close()
        
        print(f"\n🎉 Migration hoàn thành!")
        print(f"   📊 Đã thêm {added_columns} cột mới")
        print(f"   📋 Tổng cộng {len(new_columns)} cột admin")

if __name__ == "__main__":
    migrate_admin() 