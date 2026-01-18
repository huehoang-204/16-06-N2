# Script PowerShell để dọn dẹp dữ liệu không hợp lệ
# CÁCH CHẠY: .\cleanup_and_upgrade.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CLEANUP & UPGRADE QUAN_LY_TAI_SAN" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Đường dẫn đến thư mục Odoo
$odooPath = "d:\HKII_2025-2026_Class 16-06\ThucTapCNTT7\OdooProject\16-06-N2"
Set-Location $odooPath

# Database config
$dbName = "odoolab"
$dbUser = "odoo"
$dbPassword = "odoo"
$dbHost = "localhost"
$dbPort = "5432"

Write-Host "Bước 1: Dọn dẹp dữ liệu không hợp lệ..." -ForegroundColor Yellow
Write-Host ""

# Tạo file SQL tạm thời
$sqlContent = @"
-- Cleanup invalid danh_muc_ts_id
UPDATE de_xuat_mua_tai_san_line
SET danh_muc_ts_id = NULL
WHERE danh_muc_ts_id IS NOT NULL
  AND danh_muc_ts_id NOT IN (SELECT id FROM danh_muc_tai_san);

-- Show result
SELECT COUNT(*) as cleaned_records FROM de_xuat_mua_tai_san_line WHERE danh_muc_ts_id IS NULL;
"@

$sqlFile = Join-Path $odooPath "temp_cleanup.sql"
$sqlContent | Out-File -FilePath $sqlFile -Encoding UTF8

# Chạy SQL cleanup
Write-Host "Chạy SQL cleanup..." -ForegroundColor Green
$env:PGPASSWORD = $dbPassword
& psql -h $dbHost -p $dbPort -U $dbUser -d $dbName -f $sqlFile

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Cleanup thành công!" -ForegroundColor Green
} else {
    Write-Host "✗ Cleanup thất bại. Kiểm tra lỗi ở trên." -ForegroundColor Red
    Write-Host ""
    Write-Host "Nếu chưa cài PostgreSQL client tools, hãy chạy thủ công:" -ForegroundColor Yellow
    Write-Host "1. Mở pgAdmin hoặc DBeaver" -ForegroundColor Yellow
    Write-Host "2. Kết nối đến database '$dbName'" -ForegroundColor Yellow
    Write-Host "3. Chạy file: cleanup_invalid_data.sql" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Hoặc bỏ qua bước này nếu đã sửa code (code sẽ tự động xử lý)" -ForegroundColor Yellow
}

# Xóa file tạm
Remove-Item $sqlFile -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "Bước 2: Upgrade module..." -ForegroundColor Yellow
Write-Host ""

# Upgrade module
Write-Host "Đang upgrade module quan_ly_tai_san..." -ForegroundColor Green
& python odoo-bin -c odoo.conf -u quan_ly_tai_san -d $dbName --stop-after-init

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Upgrade thành công!" -ForegroundColor Green
} else {
    Write-Host "✗ Upgrade thất bại. Kiểm tra lỗi ở trên." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  HOÀN THÀNH!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Bước tiếp theo:" -ForegroundColor Yellow
Write-Host "1. Khởi động Odoo: python odoo-bin -c odoo.conf" -ForegroundColor White
Write-Host "2. Đăng nhập và kiểm tra" -ForegroundColor White
Write-Host "3. Clear browser cache (Ctrl+Shift+Del)" -ForegroundColor White
Write-Host ""
