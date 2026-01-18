#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script đơn giản để cleanup database - CHẠY NGAY!
Không cần cài thêm gì, chỉ cần psycopg2 (đã có sẵn trong Odoo)
"""

import sys
import os

# Thêm đường dẫn Odoo vào sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import psycopg2
except ImportError:
    print("Đang import psycopg2 từ Odoo...")
    # Nếu không có psycopg2, thử import từ Odoo
    try:
        from odoo.sql_db import db_connect
        HAS_ODOO = True
    except:
        print("ERROR: Không tìm thấy psycopg2. Cài đặt: pip install psycopg2-binary")
        sys.exit(1)
else:
    HAS_ODOO = False

def get_windows_host_ip():
    """Lấy IP của Windows host từ WSL"""
    try:
        with open('/etc/resolv.conf', 'r') as f:
            for line in f:
                if line.startswith('nameserver'):
                    return line.split()[1]
    except:
        pass
    return 'localhost'

def cleanup_with_psycopg2():
    """Cleanup bằng psycopg2 thuần"""
    print("="*60)
    print("CLEANUP DATABASE - PSYCOPG2")
    print("="*60)
    
    # Tự động detect Windows host IP
    windows_host = get_windows_host_ip()
    print(f"\nDetected Windows host: {windows_host}")
    
    # Config - Thử nhiều host
    hosts_to_try = [windows_host, 'localhost', '127.0.0.1', '172.18.80.1']
    
    DB_CONFIG_BASE = {
        'database': 'odoolab',
        'user': 'odoo',
        'password': 'odoo',  # Thay đổi nếu password khác
        'port': 5432
    }
    DB_CONFIG_BASE = {
        'database': 'odoolab',
        'user': 'odoo',
        'password': 'odoo',  # Thay đổi nếu password khác
        'port': 5432
    }
    
    conn = None
    # Thử kết nối với từng host
    print(f"\n1. Đang thử kết nối đến database '{DB_CONFIG_BASE['database']}'...")
    
    for host in hosts_to_try:
        try:
            print(f"   Thử kết nối: {host}:{DB_CONFIG_BASE['port']}...", end=" ")
            DB_CONFIG = {**DB_CONFIG_BASE, 'host': host}
            conn = psycopg2.connect(**DB_CONFIG)
            conn.autocommit = False
            print("✓ Thành công!")
            break
        except psycopg2.OperationalError as e:
            print(f"✗ Thất bại")
            continue
    
    if not conn:
        print(f"\n✗ KHÔNG THỂ KẾT NỐI DATABASE!")
        print("\nThử các cách sau:")
        print("1. Kiểm tra PostgreSQL đang chạy trên Windows")
        print("2. Cho phép PostgreSQL listen trên tất cả IP:")
        print("   - Mở: C:\\Program Files\\PostgreSQL\\xx\\data\\postgresql.conf")
        print("   - Tìm: listen_addresses = 'localhost'")
        print("   - Sửa: listen_addresses = '*'")
        print("   - Restart PostgreSQL")
        print("3. Hoặc dùng pgAdmin trên Windows để chạy SQL")
        return False
    
    try:
        cur = conn.cursor()
        
        # Kiểm tra trước khi cleanup
        print("\n2. Kiểm tra số lượng record bị lỗi...")
        cur.execute("""
            SELECT COUNT(*) 
            FROM de_xuat_mua_tai_san_line l
            LEFT JOIN danh_muc_tai_san d ON l.danh_muc_ts_id = d.id
            WHERE l.danh_muc_ts_id IS NOT NULL AND d.id IS NULL
        """)
        before_count = cur.fetchone()[0]
        print(f"   → Tìm thấy {before_count} records cần cleanup")
        
        if before_count == 0:
            print("\n✓ Không có dữ liệu cần cleanup!")
            cur.close()
            conn.close()
            return True
        
        # Cleanup
        print("\n3. Đang cleanup...")
        cur.execute("""
            UPDATE de_xuat_mua_tai_san_line
            SET danh_muc_ts_id = NULL
            WHERE danh_muc_ts_id IS NOT NULL
              AND danh_muc_ts_id NOT IN (SELECT id FROM danh_muc_tai_san)
        """)
        affected = cur.rowcount
        print(f"   → Đã cleanup {affected} records")
        
        # Commit
        print("\n4. Commit thay đổi...")
        conn.commit()
        print("   → Đã commit!")
        
        # Kiểm tra lại
        print("\n5. Kiểm tra lại...")
        cur.execute("""
            SELECT COUNT(*) 
            FROM de_xuat_mua_tai_san_line l
            LEFT JOIN danh_muc_tai_san d ON l.danh_muc_ts_id = d.id
            WHERE l.danh_muc_ts_id IS NOT NULL AND d.id IS NULL
        """)
        after_count = cur.fetchone()[0]
        print(f"   → Còn lại: {after_count} (phải là 0)")
        
        # Đóng kết nối
        cur.close()
        conn.close()
        
        print("\n" + "="*60)
        if after_count == 0:
            print("✓ CLEANUP THÀNH CÔNG!")
            print("="*60)
            print("\nBước tiếp theo:")
            print("1. Upgrade module: python3 odoo-bin -c odoo.conf -u quan_ly_tai_san -d odoolab --stop-after-init")
            print("2. Khởi động Odoo: python3 odoo-bin -c odoo.conf")
            print("3. Clear browser cache và test lại")
            return True
        else:
            print(f"✗ VẪN CÒN {after_count} RECORDS BỊ LỖI!")
            print("="*60)
            return False
            
    except psycopg2.OperationalError as e:
        print(f"\n✗ LỖI KẾT NỐI DATABASE: {e}")
        print("\nKiểm tra:")
        print("- PostgreSQL có đang chạy không?")
        print("- Username/password có đúng không?")
        print("- Database 'odoolab' có tồn tại không?")
        return False
    except Exception as e:
        print(f"\n✗ LỖI: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║  SCRIPT CLEANUP DỮ LIỆU KHÔNG HỢP LỆ - QUAN LY TAI SAN  ║")
    print("╚" + "="*58 + "╝")
    print("\n")
    
    success = cleanup_with_psycopg2()
    
    print("\n")
    if success:
        sys.exit(0)
    else:
        print("Nếu gặp lỗi kết nối, hãy:")
        print("1. Kiểm tra PostgreSQL đang chạy")
        print("2. Sử dụng pgAdmin để chạy SQL thủ công:")
        print("\n   UPDATE de_xuat_mua_tai_san_line")
        print("   SET danh_muc_ts_id = NULL")
        print("   WHERE danh_muc_ts_id IS NOT NULL")
        print("     AND danh_muc_ts_id NOT IN (SELECT id FROM danh_muc_tai_san);")
        print("\n")
        sys.exit(1)
