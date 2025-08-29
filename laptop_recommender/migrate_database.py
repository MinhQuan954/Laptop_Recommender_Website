#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script migration database để thêm các trường benchmark mới
Sử dụng: python migrate_database.py
"""

from app import create_app
from models import db
import sqlite3
import os

def migrate_database():
    """Migration database để thêm các trường mới"""
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
        
        print("🔄 Đang migration database...")
        
        # Danh sách các cột cần thêm
        new_columns = [
            ('battery_capacity', 'INTEGER'),
            ('battery_life_office', 'INTEGER'),
            ('battery_life_gaming', 'INTEGER'),
            ('cpu_single_core_plugged', 'INTEGER'),
            ('cpu_multi_core_plugged', 'INTEGER'),
            ('cpu_single_core_battery', 'INTEGER'),
            ('cpu_multi_core_battery', 'INTEGER'),
            ('gpu_score_plugged', 'INTEGER'),
            ('gpu_score_battery', 'INTEGER')
        ]
        
        # Kiểm tra xem bảng laptops có tồn tại không
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='laptops'")
        if not cursor.fetchone():
            print("❌ Bảng laptops không tồn tại. Tạo bảng mới...")
            db.create_all()
            print("✅ Đã tạo bảng mới")
            conn.close()
            return
        
        # Lấy danh sách cột hiện tại
        cursor.execute("PRAGMA table_info(laptops)")
        existing_columns = [column[1] for column in cursor.fetchall()]
        
        # Thêm các cột mới nếu chưa tồn tại
        added_columns = 0
        for column_name, column_type in new_columns:
            if column_name not in existing_columns:
                try:
                    cursor.execute(f"ALTER TABLE laptops ADD COLUMN {column_name} {column_type}")
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
        print(f"   📋 Tổng cộng {len(new_columns)} cột benchmark")

if __name__ == "__main__":
    migrate_database() 