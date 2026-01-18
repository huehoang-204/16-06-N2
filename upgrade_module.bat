@echo off
REM Script nâng cấp module quan_ly_tai_chinh và quan_ly_tai_san cho Windows

echo =========================================
echo NÂNG CẤP MODULE QUẢN LÝ TÀI SẢN VÀ TÀI CHÍNH
echo =========================================

REM Dừng Odoo nếu đang chạy
echo Đang kiểm tra và dừng Odoo...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *odoo*" 2>nul
timeout /t 2 >nul

REM Upgrade cả 2 module
echo Đang nâng cấp module...
python odoo-bin -c odoo.conf -u quan_ly_tai_san,quan_ly_tai_chinh -d OdooLab --stop-after-init

echo =========================================
echo HOÀN THÀNH NÂNG CẤP MODULE
echo =========================================
echo.
echo Bây giờ bạn có thể khởi động Odoo bằng lệnh:
echo python odoo-bin -c odoo.conf
pause
