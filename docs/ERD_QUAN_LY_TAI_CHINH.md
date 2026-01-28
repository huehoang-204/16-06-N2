# Sơ đồ ERD Chi tiết - Module Quản lý Tài chính

## 1. Sơ đồ ERD (Mermaid Format)

```mermaid
erDiagram
    %% ========================================
    %% BẢNG CHÍNH - QUẢN LÝ TÀI CHÍNH
    %% ========================================

    KHAU_HAO_TAI_SAN {
        int id PK
        int tai_san_id FK "Tài sản"
        int phe_duyet_mua_id FK "Phê duyệt mua"
        date ngay_bat_dau "Ngày bắt đầu"
        int so_nam_khau_hao "Số năm khấu hao"
        float gia_tri_ban_dau "Giá trị ban đầu"
        float gia_tri_khau_hao_hang_nam "KH hàng năm"
        float tong_gia_tri_khau_hao "Tổng giá trị KH"
        float gia_tri_con_lai "Giá trị còn lại"
        int thoi_gian_khau_hao "Thời gian (năm)"
        float ty_le_khau_hao "Tỷ lệ khấu hao (%)"
        varchar trang_thai "Trạng thái"
    }

    PHE_DUYET_MUA_TAI_SAN {
        int id PK
        varchar ma_phe_duyet UK "Mã phê duyệt"
        int de_xuat_mua_id FK "Đề xuất mua"
        varchar ten_de_xuat "Tên đề xuất"
        date ngay_tao "Ngày tạo"
        date ngay_de_xuat "Ngày đề xuất"
        int nguoi_de_xuat_id FK "Người đề xuất"
        int phong_ban_id FK "Phòng ban"
        float tong_gia_tri "Tổng giá trị"
        varchar don_vi_tien_te "Đơn vị tiền tệ"
        text ly_do "Lý do"
        text mo_ta "Mô tả"
        date ngay_du_kien_nhan "Ngày dự kiến nhận"
        varchar state "Trạng thái"
        int nguoi_phe_duyet_id FK "Người phê duyệt"
        date ngay_phe_duyet "Ngày phê duyệt"
        text ghi_chu_phe_duyet "Ghi chú phê duyệt"
        int tk_tai_san_id FK "TK Tài sản"
        int tk_nguon_von_id FK "TK Nguồn vốn"
        int journal_id FK "Journal"
        int but_toan_id FK "Bút toán"
    }

    PHE_DUYET_MUA_TAI_SAN_LINE {
        int id PK
        int sequence "Thứ tự"
        int phe_duyet_id FK "Phê duyệt"
        varchar ten_thiet_bi "Tên thiết bị"
        int danh_muc_ts_id FK "Danh mục TS"
        text mo_ta "Mô tả"
        text thong_so_ky_thuat "Thông số kỹ thuật"
        int so_luong "Số lượng"
        varchar don_vi_tinh "Đơn vị tính"
        float don_gia "Đơn giá"
        float thanh_tien "Thành tiền"
        varchar pp_khau_hao "PP khấu hao"
        int thoi_gian_su_dung "Thời gian SD (năm)"
        float ty_le_khau_hao "Tỷ lệ khấu hao"
        varchar nha_cung_cap "Nhà cung cấp"
    }

    BUT_TOAN {
        int id PK
        varchar so_but_toan UK "Số bút toán"
        date ngay_but_toan "Ngày bút toán"
        text mo_ta "Mô tả"
        int khau_hao_id FK "Khấu hao"
        int tai_khoan_no_id FK "TK Nợ"
        int tai_khoan_co_id FK "TK Có"
        float so_tien "Số tiền"
        varchar trang_thai "Trạng thái"
    }

    BAO_CAO_TAI_CHINH {
        int id PK
        varchar name "Tên báo cáo"
        int thang "Tháng"
        int nam "Năm"
        float doanh_thu "Doanh thu"
        float tong_chi_phi "Tổng chi phí"
        float chi_phi_khau_hao "Chi phí khấu hao"
        float chi_phi_luong "Chi phí lương"
        float chi_phi_van_phong "Chi phí văn phòng"
        float chi_phi_marketing "Chi phí marketing"
        float chi_phi_dien_nuoc "Chi phí điện nước"
        float chi_phi_khac "Chi phí khác"
        float loi_nhuan "Lợi nhuận"
        float ty_le_loi_nhuan "Tỷ lệ lợi nhuận (%)"
        varchar trang_thai "Trạng thái"
        int nguoi_tao_id FK "Người tạo"
        int nguoi_xu_ly_id FK "Người xử lý"
        datetime ngay_tao "Ngày tạo"
        datetime ngay_hoan_thanh "Ngày hoàn thành"
    }

    %% ========================================
    %% BẢNG DASHBOARD TÀI CHÍNH
    %% ========================================

    DASHBOARD_TAI_CHINH {
        int id PK
        varchar name "Tên"
        date ngay_hien_tai "Ngày hiện tại"
    }

    DASHBOARD_DEPRECIATION_TREND {
        int id PK
        int dashboard_id FK "Dashboard"
        int company_id FK "Công ty"
        varchar thang "Tháng"
        float gia_tri_khau_hao "Giá trị khấu hao"
    }

    DASHBOARD_PURCHASE_TREND {
        int id PK
        int dashboard_id FK "Dashboard"
        int company_id FK "Công ty"
        varchar thang "Tháng"
        float gia_tri_mua "Giá trị mua"
    }

    DASHBOARD_DEPARTMENT_DISTRIBUTION {
        int id PK
        int dashboard_id FK "Dashboard"
        int department_id FK "Phòng ban"
        int company_id FK "Công ty"
        float gia_tri "Giá trị"
        float ty_le "Tỷ lệ (%)"
    }

    %% ========================================
    %% BẢNG LIÊN KẾT TỪ MODULE KHÁC
    %% ========================================

    TAI_SAN {
        int id PK
        varchar ma_tai_san "Mã tài sản"
        varchar ten_tai_san "Tên tài sản"
        float gia_tri_ban_dau "Giá trị ban đầu"
        float gia_tri_hien_tai "Giá trị hiện tại"
    }

    DE_XUAT_MUA_TAI_SAN {
        int id PK
        varchar ma_de_xuat "Mã đề xuất"
        varchar ten_de_xuat "Tên đề xuất"
        float tong_gia_tri "Tổng giá trị"
        varchar trang_thai "Trạng thái"
    }

    PHONG_BAN {
        int id PK
        varchar ma_phong_ban "Mã phòng ban"
        varchar ten_phong_ban "Tên phòng ban"
    }

    DANH_MUC_TAI_SAN {
        int id PK
        varchar ma_danh_muc "Mã danh mục"
        varchar ten_danh_muc "Tên danh mục"
    }

    ACCOUNT_ACCOUNT {
        int id PK
        varchar code "Mã tài khoản"
        varchar name "Tên tài khoản"
    }

    %% ========================================
    %% QUAN HỆ NỘI BỘ MODULE TÀI CHÍNH
    %% ========================================

    KHAU_HAO_TAI_SAN ||--o{ BUT_TOAN : "generates"
    PHE_DUYET_MUA_TAI_SAN ||--o{ KHAU_HAO_TAI_SAN : "creates"
    PHE_DUYET_MUA_TAI_SAN ||--o{ PHE_DUYET_MUA_TAI_SAN_LINE : "has_lines"
    
    DASHBOARD_TAI_CHINH ||--o{ DASHBOARD_DEPRECIATION_TREND : "shows"
    DASHBOARD_TAI_CHINH ||--o{ DASHBOARD_PURCHASE_TREND : "shows"
    DASHBOARD_TAI_CHINH ||--o{ DASHBOARD_DEPARTMENT_DISTRIBUTION : "shows"

    %% ========================================
    %% QUAN HỆ VỚI MODULE KHÁC
    %% ========================================

    %% Tài sản → Tài chính
    TAI_SAN ||--o{ KHAU_HAO_TAI_SAN : "depreciated"
    
    %% Đề xuất mua → Phê duyệt
    DE_XUAT_MUA_TAI_SAN ||--o{ PHE_DUYET_MUA_TAI_SAN : "approved"
    
    %% Phòng ban → Phê duyệt
    PHONG_BAN ||--o{ PHE_DUYET_MUA_TAI_SAN : "requests"
    
    %% Danh mục → Chi tiết phê duyệt
    DANH_MUC_TAI_SAN ||--o{ PHE_DUYET_MUA_TAI_SAN_LINE : "categorizes"
    
    %% Tài khoản kế toán
    ACCOUNT_ACCOUNT ||--o{ BUT_TOAN : "debit"
    ACCOUNT_ACCOUNT ||--o{ BUT_TOAN : "credit"
    ACCOUNT_ACCOUNT ||--o{ PHE_DUYET_MUA_TAI_SAN : "asset_account"
    ACCOUNT_ACCOUNT ||--o{ PHE_DUYET_MUA_TAI_SAN : "source_account"
```

## 2. Mô hình quan hệ dạng Text

```
                                    ┌─────────────────────┐
                                    │   ACCOUNT_ACCOUNT   │
                                    │   (Tài khoản KT)    │
                                    └──────────┬──────────┘
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    │ tai_khoan_no_id          │ tai_khoan_co_id          │
                    │ tk_tai_san_id            │ tk_nguon_von_id          │
                    ▼                          ▼                          │
┌─────────────────────────────┐    ┌─────────────────────────────┐        │
│       BUT_TOAN              │    │   PHE_DUYET_MUA_TAI_SAN     │◄───────┘
│   (Bút toán kế toán)        │    │   (Phê duyệt mua tài sản)   │
├─────────────────────────────┤    ├─────────────────────────────┤
│ • so_but_toan               │    │ • ma_phe_duyet              │
│ • ngay_but_toan             │◄───│ • nguoi_de_xuat_id          │
│ • khau_hao_id (FK)          │    │ • nguoi_phe_duyet_id        │
│ • tai_khoan_no_id (FK)      │    │ • phong_ban_id (FK)         │
│ • tai_khoan_co_id (FK)      │    │ • de_xuat_mua_id (FK)       │
│ • so_tien                   │    │ • state                     │
│ • trang_thai                │    │ • tong_gia_tri              │
└─────────────────────────────┘    └──────────────┬──────────────┘
              ▲                                   │
              │ khau_hao_id                       │ phe_duyet_id
              │                                   ▼
┌─────────────────────────────┐    ┌─────────────────────────────┐
│     KHAU_HAO_TAI_SAN        │    │ PHE_DUYET_MUA_TAI_SAN_LINE  │
│   (Khấu hao tài sản)        │    │ (Chi tiết phê duyệt mua)    │
├─────────────────────────────┤    ├─────────────────────────────┤
│ • tai_san_id (FK)           │    │ • ten_thiet_bi              │
│ • phe_duyet_mua_id (FK)     │    │ • danh_muc_ts_id (FK)       │
│ • ngay_bat_dau              │    │ • so_luong                  │
│ • so_nam_khau_hao           │    │ • don_gia                   │
│ • gia_tri_ban_dau           │    │ • thanh_tien                │
│ • gia_tri_khau_hao_hang_nam │    │ • pp_khau_hao               │
│ • tong_gia_tri_khau_hao     │    │ • thoi_gian_su_dung         │
│ • gia_tri_con_lai           │    └─────────────────────────────┘
│ • trang_thai                │                   ▲
└──────────────┬──────────────┘                   │
               │ tai_san_id                       │ danh_muc_ts_id
               ▼                                  │
┌─────────────────────────────┐    ┌──────────────┴──────────────┐
│         TAI_SAN             │    │     DANH_MUC_TAI_SAN        │
│   (Module Quản lý TS)       │    │   (Module Quản lý TS)       │
└─────────────────────────────┘    └─────────────────────────────┘
```

## 3. Chi tiết các bảng

### 3.1. Khấu hao Tài sản (`khau_hao_tai_san`)
Bảng quản lý việc tính khấu hao cho từng tài sản.

| Field | Type | Mô tả | FK |
|-------|------|-------|-----|
| id | Integer | Khóa chính | - |
| tai_san_id | Integer | Tài sản được khấu hao | → tai_san |
| phe_duyet_mua_id | Integer | Phê duyệt mua liên quan | → phe_duyet_mua_tai_san |
| ngay_bat_dau | Date | Ngày bắt đầu khấu hao | - |
| so_nam_khau_hao | Integer | Số năm khấu hao | - |
| gia_tri_ban_dau | Float | Giá trị ban đầu | - |
| gia_tri_khau_hao_hang_nam | Float | Khấu hao mỗi năm | - |
| tong_gia_tri_khau_hao | Float | Tổng đã khấu hao | - |
| gia_tri_con_lai | Float | Giá trị còn lại | - |
| trang_thai | Selection | nhap/dang_khau_hao/hoan_thanh | - |

### 3.2. Phê duyệt Mua Tài sản (`phe_duyet_mua_tai_san`)
Bảng quản lý quy trình phê duyệt mua sắm tài sản.

| Field | Type | Mô tả | FK |
|-------|------|-------|-----|
| id | Integer | Khóa chính | - |
| ma_phe_duyet | Char | Mã phê duyệt (unique) | - |
| de_xuat_mua_id | Integer | Đề xuất mua liên quan | → de_xuat_mua_tai_san |
| phong_ban_id | Integer | Phòng ban đề xuất | → phong_ban |
| nguoi_de_xuat_id | Integer | Người đề xuất | → res.users |
| nguoi_phe_duyet_id | Integer | Người phê duyệt | → res.users |
| tong_gia_tri | Float | Tổng giá trị | - |
| state | Selection | draft/pending/approved/rejected | - |
| tk_tai_san_id | Integer | Tài khoản tài sản | → account.account |
| tk_nguon_von_id | Integer | Tài khoản nguồn vốn | → account.account |

### 3.3. Chi tiết Phê duyệt (`phe_duyet_mua_tai_san_line`)
Bảng chi tiết các thiết bị trong đơn phê duyệt.

| Field | Type | Mô tả | FK |
|-------|------|-------|-----|
| id | Integer | Khóa chính | - |
| phe_duyet_id | Integer | Phê duyệt cha | → phe_duyet_mua_tai_san |
| ten_thiet_bi | Char | Tên thiết bị | - |
| danh_muc_ts_id | Integer | Danh mục tài sản | → danh_muc_tai_san |
| so_luong | Integer | Số lượng | - |
| don_gia | Float | Đơn giá | - |
| thanh_tien | Float | Thành tiền (computed) | - |
| pp_khau_hao | Selection | Phương pháp khấu hao | - |
| thoi_gian_su_dung | Integer | Thời gian sử dụng (năm) | - |

### 3.4. Bút toán (`but_toan`)
Bảng ghi nhận các bút toán kế toán.

| Field | Type | Mô tả | FK |
|-------|------|-------|-----|
| id | Integer | Khóa chính | - |
| so_but_toan | Char | Số bút toán (unique) | - |
| ngay_but_toan | Date | Ngày bút toán | - |
| khau_hao_id | Integer | Khấu hao liên quan | → khau_hao_tai_san |
| tai_khoan_no_id | Integer | Tài khoản Nợ | → account.account |
| tai_khoan_co_id | Integer | Tài khoản Có | → account.account |
| so_tien | Float | Số tiền | - |
| trang_thai | Selection | nhap/da_ghi_so | - |

### 3.5. Báo cáo Tài chính (`bao_cao_tai_chinh`)
Bảng lưu trữ báo cáo tài chính theo tháng/năm.

| Field | Type | Mô tả | FK |
|-------|------|-------|-----|
| id | Integer | Khóa chính | - |
| name | Char | Tên báo cáo | - |
| thang | Integer | Tháng (1-12) | - |
| nam | Integer | Năm | - |
| doanh_thu | Float | Doanh thu | - |
| tong_chi_phi | Float | Tổng chi phí | - |
| chi_phi_khau_hao | Float | Chi phí khấu hao | - |
| chi_phi_luong | Float | Chi phí lương | - |
| loi_nhuan | Float | Lợi nhuận | - |
| ty_le_loi_nhuan | Float | Tỷ lệ lợi nhuận (%) | - |
| trang_thai | Selection | nhap/da_duyet | - |

## 4. Luồng dữ liệu chính

```
[Đề xuất mua tài sản]
        │
        │ Gửi duyệt
        ▼
┌───────────────────────┐
│ PHE_DUYET_MUA_TAI_SAN │ ◄─── Phòng ban đề xuất
│                       │ ◄─── Người phê duyệt
│   state: pending      │
└───────────┬───────────┘
            │
            │ Phê duyệt
            ▼
┌───────────────────────┐
│ PHE_DUYET_MUA_TAI_SAN │
│   state: approved     │
└───────────┬───────────┘
            │
            │ Tạo tài sản + Tạo khấu hao
            ▼
┌───────────────────────┐      ┌───────────────────────┐
│      TAI_SAN          │─────►│   KHAU_HAO_TAI_SAN    │
│  (Module Tài sản)     │      │ trang_thai: dang_kh   │
└───────────────────────┘      └───────────┬───────────┘
                                           │
                                           │ Hàng tháng/năm
                                           ▼
                               ┌───────────────────────┐
                               │       BUT_TOAN        │
                               │ Nợ: Chi phí khấu hao  │
                               │ Có: Khấu hao lũy kế   │
                               └───────────────────────┘
```

## 5. Thống kê Module Tài chính

| Bảng | Số field | Quan hệ FK | Vai trò |
|------|----------|------------|---------|
| `khau_hao_tai_san` | 17 | 2 | Quản lý khấu hao |
| `phe_duyet_mua_tai_san` | 22 | 6 | Phê duyệt mua sắm |
| `phe_duyet_mua_tai_san_line` | 19 | 2 | Chi tiết phê duyệt |
| `but_toan` | 13 | 3 | Bút toán kế toán |
| `bao_cao_tai_chinh` | 23 | 2 | Báo cáo tài chính |
| `dashboard_tai_chinh` | 7 | 0 | Dashboard |
| `dashboard_depreciation_trend` | - | 2 | Xu hướng khấu hao |
| `dashboard_purchase_trend` | - | 2 | Xu hướng mua sắm |
| `dashboard_department_distribution` | - | 3 | Phân bổ theo phòng ban |
