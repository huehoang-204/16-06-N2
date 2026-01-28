#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tạo tài khoản web cho tất cả nhân viên
Chạy: python3 scripts/create_employee_accounts.py
"""

import sys
import os

# Thêm path của Odoo
sys.path.insert(0, '/home/hue/btl2/16-06-N2')

import odoo
from odoo import api, SUPERUSER_ID
import hashlib

def hash_password(password):
    """Hash mật khẩu sử dụng SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_accounts():
    # Cấu hình Odoo
    odoo.tools.config.parse_config(['--config=/home/hue/btl2/16-06-N2/odoo.conf'])
    
    # Kết nối database
    db_name = 'btl2'
    registry = odoo.registry(db_name)
    
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        NhanVien = env['nhan_vien']
        
        # Lấy tất cả nhân viên
        employees = NhanVien.search([])
        
        print(f"Tìm thấy {len(employees)} nhân viên")
        print("=" * 60)
        
        accounts = []
        
        for emp in employees:
            # Tạo username từ mã định danh (lowercase)
            username = emp.ma_dinh_danh.lower()
            # Mật khẩu mặc định: 123456
            default_password = '123456'
            password_hash = hash_password(default_password)
            
            # Cập nhật thông tin đăng nhập
            emp.write({
                'web_username': username,
                'web_password_hash': password_hash,
                'is_web_active': True,
            })
            
            accounts.append({
                'id': emp.id,
                'ma_dinh_danh': emp.ma_dinh_danh,
                'ho_ten': emp.ho_ten,
                'username': username,
                'password': default_password,
            })
            
            print(f"✓ {emp.ho_ten} ({emp.ma_dinh_danh})")
            print(f"  Username: {username}")
            print(f"  Password: {default_password}")
            print()
        
        # Commit transaction
        cr.commit()
        
        print("=" * 60)
        print(f"Đã tạo tài khoản cho {len(accounts)} nhân viên!")
        print()
        print("DANH SÁCH TÀI KHOẢN:")
        print("-" * 60)
        print(f"{'Username':<15} {'Password':<15} {'Họ tên':<20}")
        print("-" * 60)
        for acc in accounts:
            print(f"{acc['username']:<15} {acc['password']:<15} {acc['ho_ten']:<20}")
        
        return accounts

if __name__ == '__main__':
    create_accounts()
