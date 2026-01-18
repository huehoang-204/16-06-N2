#!/bin/bash
# Script nâng cấp module quan_ly_tai_chinh

echo "========================================="
echo "NÂNG CẤP MODULE QUẢN LÝ TÀI CHÍNH"
echo "========================================="

# Dừng Odoo nếu đang chạy
echo "Đang kiểm tra và dừng Odoo..."
pkill -f "odoo-bin"

# Chờ một chút
sleep 2

# Upgrade module
echo "Đang nâng cấp module..."
python3 odoo-bin -c odoo.conf -u quan_ly_tai_chinh -d OdooLab --stop-after-init

echo "========================================="
echo "HOÀN THÀNH NÂNG CẤP MODULE"
echo "========================================="
echo ""
echo "Bây giờ bạn có thể khởi động Odoo bằng lệnh:"
echo "python3 odoo-bin -c odoo.conf"
