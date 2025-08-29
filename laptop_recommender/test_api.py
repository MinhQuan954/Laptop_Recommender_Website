#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script test API compare
Sử dụng: python test_api.py
"""

import requests
import json

def test_api():
    """Test API compare data"""
    base_url = "http://localhost:5000"
    
    print("🧪 TESTING API COMPARE")
    print("=" * 50)
    
    # Test 1: API với mode plugged
    print("1. Test API với mode 'plugged':")
    url = f"{base_url}/api/compare_data?id=1&id=2&mode=plugged"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print("✅ Thành công!")
            print(f"   CPU Single Core: {len(data['cpu_single_core'])} items")
            print(f"   CPU Multi Core: {len(data['cpu_multi_core'])} items")
            print(f"   GPU Score: {len(data['gpu_score'])} items")
            
            # Hiển thị dữ liệu mẫu
            if data['cpu_single_core']:
                print(f"   Ví dụ CPU Single Core: {data['cpu_single_core'][0]}")
        else:
            print(f"❌ Lỗi: {response.status_code}")
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")
    
    print()
    
    # Test 2: API với mode battery
    print("2. Test API với mode 'battery':")
    url = f"{base_url}/api/compare_data?id=1&id=2&mode=battery"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print("✅ Thành công!")
            print(f"   CPU Single Core: {len(data['cpu_single_core'])} items")
            print(f"   CPU Multi Core: {len(data['cpu_multi_core'])} items")
            print(f"   GPU Score: {len(data['gpu_score'])} items")
            
            # Hiển thị dữ liệu mẫu
            if data['cpu_single_core']:
                print(f"   Ví dụ CPU Single Core: {data['cpu_single_core'][0]}")
        else:
            print(f"❌ Lỗi: {response.status_code}")
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")
    
    print()
    
    # Test 3: So sánh dữ liệu
    print("3. So sánh dữ liệu plugged vs battery:")
    try:
        response_plugged = requests.get(f"{base_url}/api/compare_data?id=1&id=2&mode=plugged")
        response_battery = requests.get(f"{base_url}/api/compare_data?id=1&id=2&mode=battery")
        
        if response_plugged.status_code == 200 and response_battery.status_code == 200:
            data_plugged = response_plugged.json()
            data_battery = response_battery.json()
            
            print("✅ So sánh thành công!")
            
            # So sánh CPU Single Core
            if data_plugged['cpu_single_core'] and data_battery['cpu_single_core']:
                plugged_score = data_plugged['cpu_single_core'][0]['score']
                battery_score = data_battery['cpu_single_core'][0]['score']
                print(f"   CPU Single Core - Plugged: {plugged_score}, Battery: {battery_score}")
                print(f"   Chênh lệch: {plugged_score - battery_score}")
            
            # So sánh GPU
            if data_plugged['gpu_score'] and data_battery['gpu_score']:
                plugged_gpu = data_plugged['gpu_score'][0]['score']
                battery_gpu = data_battery['gpu_score'][0]['score']
                print(f"   GPU Score - Plugged: {plugged_gpu}, Battery: {battery_gpu}")
                print(f"   Chênh lệch: {plugged_gpu - battery_gpu}")
        else:
            print("❌ Lỗi khi so sánh dữ liệu")
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")
    
    print()
    print("🎉 Test hoàn thành!")

if __name__ == "__main__":
    test_api() 