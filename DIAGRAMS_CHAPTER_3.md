# TẬP HỢP CÁC SƠ ĐỒ CHO CHƯƠNG 3
## Phân tích, Thiết kế và Triển khai Hệ thống

**Hướng dẫn sử dụng:**
- Các sơ đồ được vẽ bằng Mermaid
- Để xuất hình ảnh: 
  1. Truy cập https://mermaid.live
  2. Copy code Mermaid vào
  3. Xuất PNG/SVG
- Hoặc sử dụng VS Code extension "Markdown Preview Mermaid Support"

---

# HÌNH 3.1: SƠ ĐỒ KIẾN TRÚC TỔNG THỂ HỆ THỐNG

```mermaid
flowchart TB
    subgraph CLIENT["🖥️ CLIENT LAYER"]
        WEB["Web Browser<br/>Chrome/Firefox/Edge"]
        MOBILE["Mobile App<br/>(Optional)"]
    end

    subgraph PRESENTATION["📱 PRESENTATION LAYER"]
        QWEB["QWeb Templates"]
        OWL["OWL Components<br/>(Dashboard, Charts)"]
        CSS["CSS/SCSS<br/>Styling"]
        JS["JavaScript<br/>Controllers"]
    end

    subgraph APPLICATION["⚙️ APPLICATION LAYER - ODOO 15"]
        subgraph MODULES["Custom Modules"]
            M1["📦 quan_ly_tai_san<br/>Module Quản lý Tài sản"]
            M2["📦 quan_ly_tai_chinh<br/>Module Quản lý Tài chính"]
        end
        
        subgraph CORE["Odoo Core"]
            ORM["ORM Framework"]
            SECURITY["Security Manager"]
            WORKFLOW["Workflow Engine"]
            API["API Controllers"]
        end
        
        subgraph DEPENDS["Base Modules"]
            BASE["base"]
            HR["hr/nhan_su"]
            ACCOUNT["account"]
            MAIL["mail"]
        end
    end

    subgraph DATA["💾 DATA LAYER"]
        PG["PostgreSQL 12+<br/>Database"]
        ATTACH["File Storage<br/>Attachments"]
    end

    WEB --> QWEB
    MOBILE --> API
    QWEB --> OWL
    OWL --> JS
    CSS --> QWEB
    
    JS --> M1
    JS --> M2
    
    M1 <-.->|"Tích hợp"| M2
    M1 --> ORM
    M2 --> ORM
    
    CORE --> DEPENDS
    ORM --> PG
    ORM --> ATTACH
    
    SECURITY --> ORM
    WORKFLOW --> ORM

    classDef clientStyle fill:#e1f5fe,stroke:#01579b
    classDef presentStyle fill:#f3e5f5,stroke:#4a148c
    classDef appStyle fill:#e8f5e9,stroke:#1b5e20
    classDef dataStyle fill:#fff3e0,stroke:#e65100
    
    class WEB,MOBILE clientStyle
    class QWEB,OWL,CSS,JS presentStyle
    class M1,M2,ORM,SECURITY,WORKFLOW,API,BASE,HR,ACCOUNT,MAIL appStyle
    class PG,ATTACH dataStyle
```

---

# HÌNH 3.2: SƠ ĐỒ USE CASE TỔNG QUÁT

```mermaid
flowchart TB
    subgraph SYSTEM["HỆ THỐNG QUẢN LÝ TÀI SẢN VÀ TÀI CHÍNH"]
        
        subgraph UC_ASSET["Module Quản lý Tài sản"]
            UC1["🔸 Quản lý danh mục<br/>tài sản"]
            UC2["🔸 Quản lý tài sản<br/>cụ thể"]
            UC3["🔸 Phân bổ tài sản<br/>cho phòng ban"]
            UC4["🔸 Tạo đề xuất<br/>mua tài sản"]
            UC5["🔸 Quản lý mượn/trả<br/>tài sản"]
            UC6["🔸 Kiểm kê tài sản"]
            UC7["🔸 Luân chuyển<br/>tài sản"]
            UC8["🔸 Thanh lý tài sản"]
            UC9["🔸 Xem Dashboard<br/>tổng quan"]
        end
        
        subgraph UC_FINANCE["Module Quản lý Tài chính"]
            UC10["🔹 Phê duyệt đề xuất<br/>mua tài sản"]
            UC11["🔹 Tạo tài sản<br/>tự động"]
            UC12["🔹 Quản lý khấu hao<br/>tài sản"]
            UC13["🔹 Ghi bút toán<br/>kế toán"]
            UC14["🔹 Quản lý tài khoản<br/>quản trị"]
            UC15["🔹 Tạo báo cáo<br/>tài chính"]
            UC16["🔹 Xem Dashboard<br/>tài chính"]
        end
    end
    
    NV["👤 Nhân viên"]
    QLTS["👤 Quản lý<br/>Tài sản"]
    QLTC["👤 Quản lý<br/>Tài chính"]
    ADMIN["👤 Admin"]
    
    NV --> UC4
    NV --> UC5
    NV --> UC9
    
    QLTS --> UC1
    QLTS --> UC2
    QLTS --> UC3
    QLTS --> UC5
    QLTS --> UC6
    QLTS --> UC7
    QLTS --> UC8
    QLTS --> UC9
    
    QLTC --> UC10
    QLTC --> UC11
    QLTC --> UC12
    QLTC --> UC13
    QLTC --> UC14
    QLTC --> UC15
    QLTC --> UC16
    
    ADMIN --> UC1
    ADMIN --> UC2
    ADMIN --> UC3
    ADMIN --> UC10
    ADMIN --> UC16
    
    UC4 -.->|"<<extend>>"| UC10
    UC10 -.->|"<<include>>"| UC11
    UC10 -.->|"<<include>>"| UC12
    UC10 -.->|"<<include>>"| UC13

    classDef actorStyle fill:#bbdefb,stroke:#1565c0
    classDef assetStyle fill:#c8e6c9,stroke:#2e7d32
    classDef financeStyle fill:#ffe0b2,stroke:#ef6c00
    
    class NV,QLTS,QLTC,ADMIN actorStyle
    class UC1,UC2,UC3,UC4,UC5,UC6,UC7,UC8,UC9 assetStyle
    class UC10,UC11,UC12,UC13,UC14,UC15,UC16 financeStyle
```

---

# HÌNH 3.3: SƠ ĐỒ ERD TỔNG QUAN

```mermaid
erDiagram
    %% ==================== MODULE QUAN_LY_TAI_SAN ====================
    
    danh_muc_tai_san ||--o{ tai_san : "chứa"
    tai_san ||--o{ phan_bo_tai_san : "phân_bổ"
    tai_san ||--o{ lich_su_khau_hao : "có"
    tai_san ||--o{ lich_su_ky_thuat : "có"
    tai_san ||--o{ thanh_ly_tai_san : "thanh_lý"
    
    phan_bo_tai_san }o--|| phong_ban : "thuộc"
    phan_bo_tai_san }o--|| nhan_vien : "sử_dụng"
    
    kiem_ke_tai_san ||--o{ kiem_ke_tai_san_line : "chứa"
    kiem_ke_tai_san_line }o--|| phan_bo_tai_san : "kiểm_kê"
    
    luan_chuyen_tai_san ||--o{ luan_chuyen_tai_san_line : "chứa"
    luan_chuyen_tai_san_line }o--|| phan_bo_tai_san : "luân_chuyển"
    
    don_muon_tai_san ||--o{ don_muon_tai_san_line : "chứa"
    don_muon_tai_san_line }o--|| phan_bo_tai_san : "mượn"
    
    muon_tra_tai_san ||--o{ muon_tra_tai_san_line : "chứa"
    muon_tra_tai_san_line }o--|| phan_bo_tai_san : "quản_lý"
    muon_tra_tai_san }o--|| don_muon_tai_san : "từ"
    
    de_xuat_mua_tai_san ||--o{ de_xuat_mua_tai_san_line : "chứa"
    
    %% ==================== MODULE QUAN_LY_TAI_CHINH ====================
    
    de_xuat_mua_tai_san ||--|| phe_duyet_mua_tai_san : "tạo"
    phe_duyet_mua_tai_san ||--o{ phe_duyet_mua_tai_san_line : "chứa"
    phe_duyet_mua_tai_san ||--o{ tai_san : "tạo_tài_sản"
    phe_duyet_mua_tai_san ||--o{ tai_khoan_quan_tri : "ghi_nhận"
    
    khau_hao_tai_san }o--|| tai_san : "khấu_hao"
    khau_hao_tai_san }o--|| phe_duyet_mua_tai_san : "từ"
    khau_hao_tai_san ||--o{ lich_khau_hao : "lịch"
    
    but_toan }o--|| khau_hao_tai_san : "ghi_nhận"

    %% ==================== ENTITIES ====================
    
    danh_muc_tai_san {
        int id PK
        char ma_danh_muc_ts UK
        char ten_danh_muc_ts
        char mo_ta_danh_muc_ts
        int so_luong_tong
    }
    
    tai_san {
        int id PK
        char ma_tai_san UK
        char ten_tai_san
        date ngay_mua_ts
        float gia_tri_ban_dau
        float gia_tri_hien_tai
        int danh_muc_ts_id FK
        selection pp_khau_hao
        selection trang_thai_thanh_ly
    }
    
    phan_bo_tai_san {
        int id PK
        int tai_san_id FK
        int phong_ban_id FK
        int nhan_vien_su_dung_id FK
        date ngay_phat
        selection trang_thai
        selection tinh_trang
    }
    
    de_xuat_mua_tai_san {
        int id PK
        char ma_de_xuat UK
        char ten_de_xuat
        date ngay_de_xuat
        int nguoi_de_xuat_id FK
        int phong_ban_id FK
        float tong_gia_tri
        selection state
    }
    
    phe_duyet_mua_tai_san {
        int id PK
        char ma_phe_duyet UK
        int de_xuat_mua_id FK
        date ngay_phe_duyet
        int nguoi_phe_duyet_id FK
        selection state
    }
    
    khau_hao_tai_san {
        int id PK
        int tai_san_id FK
        int phe_duyet_mua_id FK
        date ngay_bat_dau
        float gia_tri_ban_dau
        int so_nam_khau_hao
        selection trang_thai
    }
```

---

# HÌNH 3.4: SƠ ĐỒ ERD CHI TIẾT - MODULE QUẢN LÝ TÀI SẢN

```mermaid
erDiagram
    danh_muc_tai_san {
        int id PK "Khóa chính"
        char ma_danh_muc_ts UK "Mã loại tài sản - VD: DMTS001"
        char ten_danh_muc_ts "Tên loại tài sản"
        char mo_ta_danh_muc_ts "Mô tả chi tiết"
        int so_luong_tong "Computed - Số lượng tài sản"
    }

    tai_san {
        int id PK "Khóa chính"
        char ma_tai_san UK "Mã tài sản - VD: TS-00001"
        char ten_tai_san "Tên tài sản"
        date ngay_mua_ts "Ngày mua tài sản"
        selection don_vi_tien_te "vnd hoặc usd"
        float gia_tri_ban_dau "Giá trị ban đầu"
        float gia_tri_hien_tai "Giá trị còn lại"
        int danh_muc_ts_id FK "FK - Danh mục tài sản"
        binary giay_to_tai_san "File đính kèm"
        image hinh_anh "Hình ảnh tài sản"
        selection pp_khau_hao "straight-line/degressive/none"
        int thoi_gian_su_dung "Số năm đã sử dụng"
        int thoi_gian_toi_da "Số năm tối đa"
        float ty_le_khau_hao "Tỷ lệ khấu hao %"
        char don_vi_tinh "Đơn vị tính"
        char ghi_chu "Ghi chú"
        selection trang_thai_thanh_ly "Computed - Trạng thái"
    }

    phan_bo_tai_san {
        int id PK "Khóa chính"
        int tai_san_id FK "FK - Tài sản"
        int phong_ban_id FK "FK - Phòng ban"
        int nhan_vien_su_dung_id FK "FK - Nhân viên sử dụng"
        date ngay_phat "Ngày phân bổ"
        selection trang_thai "in-use/not-in-use"
        selection tinh_trang "binh_thuong/dang_muon/hu_hong/mat"
        int vi_tri_tai_san_id FK "FK - Vị trí thực tế"
        char ghi_chu "Ghi chú"
    }

    de_xuat_mua_tai_san {
        int id PK "Khóa chính"
        char ma_de_xuat UK "Mã đề xuất - Auto"
        char ten_de_xuat "Tiêu đề đề xuất"
        date ngay_de_xuat "Ngày tạo đề xuất"
        int nguoi_de_xuat_id FK "FK - Người đề xuất"
        int phong_ban_id FK "FK - Phòng ban"
        float tong_gia_tri "Computed - Tổng tiền"
        selection don_vi_tien_te "vnd/usd"
        text ly_do "Lý do đề xuất"
        html mo_ta "Mô tả chi tiết"
        selection state "draft/submitted/waiting_approval/approved/rejected/cancelled"
        date ngay_du_kien_nhan "Ngày dự kiến nhận"
        int phe_duyet_id FK "FK - Đơn phê duyệt"
    }

    de_xuat_mua_tai_san_line {
        int id PK "Khóa chính"
        int de_xuat_id FK "FK - Đề xuất cha"
        char ten_thiet_bi "Tên thiết bị"
        int danh_muc_ts_id FK "FK - Danh mục"
        text mo_ta "Mô tả"
        text thong_so_ky_thuat "Thông số kỹ thuật"
        int so_luong "Số lượng"
        char don_vi_tinh "Đơn vị tính"
        float don_gia "Đơn giá"
        float thanh_tien "Computed - Thành tiền"
        selection pp_khau_hao "Phương pháp khấu hao"
        int thoi_gian_su_dung "Thời gian sử dụng (năm)"
        float ty_le_khau_hao "Tỷ lệ khấu hao"
        char nha_cung_cap "Nhà cung cấp"
    }

    don_muon_tai_san {
        int id PK "Khóa chính"
        char ma_don_muon UK "Mã đơn mượn - Auto"
        char ten_don_muon "Tên đơn mượn"
        int phong_ban_cho_muon_id FK "FK - Phòng ban cho mượn"
        datetime thoi_gian_muon "Thời gian bắt đầu mượn"
        datetime thoi_gian_tra "Thời gian trả dự kiến"
        int nhan_vien_muon_id FK "FK - Nhân viên mượn"
        text ly_do "Lý do mượn"
        selection trang_thai "nhap/cho_duyet/da_duyet/dang_muon/da_tra/tu_choi/huy"
        int nguoi_duyet_id FK "FK - Người duyệt"
        text ghi_chu "Ghi chú"
    }

    don_muon_tai_san_line {
        int id PK "Khóa chính"
        int don_muon_id FK "FK - Đơn mượn cha"
        int phan_bo_tai_san_id FK "FK - Tài sản mượn"
        int so_luong "Số lượng mượn"
        selection tinh_trang_truoc_muon "tot/binh_thuong/cu/hu_hong_nhe"
        selection tinh_trang_sau_tra "tot/binh_thuong/hu_hong/mat"
        datetime thoi_gian_cho_muon "Thời gian cho mượn thực tế"
        datetime thoi_gian_tra_thuc_te "Thời gian trả thực tế"
        selection trang_thai_line "cho_muon/dang_muon/da_tra"
        char ghi_chu "Ghi chú"
    }

    muon_tra_tai_san {
        int id PK "Khóa chính"
        char ma_phieu_muon_tra UK "Mã phiếu - Auto"
        char ten_phieu_muon_tra "Tên phiếu"
        int ma_don_muon_id FK "FK - Đơn mượn gốc"
        int phong_ban_cho_muon_id FK "FK - Phòng ban cho mượn"
        int nhan_vien_muon_id FK "FK - Nhân viên mượn"
        datetime thoi_gian_muon "Thời gian mượn dự kiến"
        datetime thoi_gian_muon_thuc_te "Thời gian mượn thực tế"
        datetime thoi_gian_tra_du_kien "Thời gian trả dự kiến"
        datetime thoi_gian_tra_thuc_te "Thời gian trả thực tế"
        text ly_do_muon "Lý do mượn"
        selection trang_thai "cho_duyet/da_duyet/dang_muon/da_tra/tu_choi"
    }

    muon_tra_tai_san_line {
        int id PK "Khóa chính"
        int muon_tra_id FK "FK - Phiếu mượn trả cha"
        int phan_bo_tai_san_id FK "FK - Tài sản"
        int so_luong "Số lượng"
        char ghi_chu "Ghi chú"
    }

    kiem_ke_tai_san {
        int id PK "Khóa chính"
        char ma_phieu_kiem_ke UK "Mã phiếu - KKTS-xxx"
        char ten_phieu_kiem_ke "Tên phiếu"
        int phong_ban_id FK "FK - Phòng ban kiểm kê"
        int nhan_vien_kiem_ke_id FK "FK - Người kiểm kê"
        datetime thoi_gian_tao "Thời gian tạo phiếu"
        char trang_thai_phieu "Computed - Đã/Chưa kiểm kê"
        char ghi_chu "Ghi chú"
    }

    kiem_ke_tai_san_line {
        int id PK "Khóa chính"
        int kiem_ke_tai_san_id FK "FK - Phiếu kiểm kê cha"
        int phan_bo_tai_san_id FK "FK - Tài sản kiểm kê"
        int so_luong_thuc_te "Số lượng thực tế"
        int so_luong_ly_thuyet "Số lượng sổ sách - Default 1"
        char dvt "Related - Đơn vị tính"
        selection trang_thai "not-finished/finished"
        selection trang_thai_tai_san "good/broken/lost"
        char ghi_chu "Ghi chú tình trạng"
    }

    luan_chuyen_tai_san {
        int id PK "Khóa chính"
        char ma_phieu_luan_chuyen UK "Mã phiếu - LCTS-xxx"
        int bo_phan_nguon FK "FK - Bộ phận hiện tại"
        int bo_phan_dich FK "FK - Bộ phận chuyển đến"
        datetime thoi_gian_luan_chuyen "Thời gian luân chuyển"
        char ghi_chu "Lý do luân chuyển"
    }

    luan_chuyen_tai_san_line {
        int id PK "Khóa chính"
        int luan_chuyen_id FK "FK - Phiếu luân chuyển cha"
        int phan_bo_tai_san_id FK "FK - Tài sản luân chuyển"
        int so_luong "Số lượng - Default 1"
        char ghi_chu "Ghi chú"
    }

    thanh_ly_tai_san {
        int id PK "Khóa chính"
        char ma_thanh_ly UK "Mã thanh lý - TL-xxx"
        selection hanh_dong "ban/huy"
        int tai_san_id FK "FK - Tài sản thanh lý"
        int nguoi_thanh_ly_id FK "FK - Người thực hiện"
        datetime thoi_gian_thanh_ly "Thời gian thanh lý"
        char ly_do_thanh_ly "Lý do"
        float gia_ban "Giá bán"
        float gia_goc "Computed - Giá gốc"
    }

    lich_su_khau_hao {
        int id PK "Khóa chính"
        char ma_phieu_khau_hao UK "Mã phiếu - KHTS-xxx"
        int ma_ts FK "FK - Tài sản"
        datetime ngay_khau_hao "Ngày khấu hao"
        float gia_tri_hien_tai "Related - Giá trị hiện tại"
        float so_tien_khau_hao "Số tiền khấu hao"
        float gia_tri_con_lai "Giá trị còn lại"
        selection loai_phieu "automatic/manual"
        char ghi_chu "Ghi chú"
    }

    lich_su_ky_thuat {
        int id PK "Khóa chính"
        int tai_san_id FK "FK - Tài sản"
        char noi_dung "Nội dung ghi nhận"
        date ngay "Ngày ghi nhận"
        char ghi_chu "Ghi chú"
    }

    %% RELATIONSHIPS
    danh_muc_tai_san ||--o{ tai_san : "1-N"
    tai_san ||--o{ phan_bo_tai_san : "1-N"
    tai_san ||--o{ lich_su_khau_hao : "1-N"
    tai_san ||--o{ lich_su_ky_thuat : "1-N"
    tai_san ||--o{ thanh_ly_tai_san : "1-1"
    
    de_xuat_mua_tai_san ||--o{ de_xuat_mua_tai_san_line : "1-N"
    
    don_muon_tai_san ||--o{ don_muon_tai_san_line : "1-N"
    don_muon_tai_san_line }o--|| phan_bo_tai_san : "N-1"
    
    muon_tra_tai_san ||--o{ muon_tra_tai_san_line : "1-N"
    muon_tra_tai_san }o--|| don_muon_tai_san : "N-1"
    muon_tra_tai_san_line }o--|| phan_bo_tai_san : "N-1"
    
    kiem_ke_tai_san ||--o{ kiem_ke_tai_san_line : "1-N"
    kiem_ke_tai_san_line }o--|| phan_bo_tai_san : "N-1"
    
    luan_chuyen_tai_san ||--o{ luan_chuyen_tai_san_line : "1-N"
    luan_chuyen_tai_san_line }o--|| phan_bo_tai_san : "N-1"
```

---

# HÌNH 3.5 (Part 2): SƠ ĐỒ ERD CHI TIẾT - MODULE QUẢN LÝ TÀI CHÍNH

```mermaid
erDiagram
    phe_duyet_mua_tai_san {
        int id PK "Khóa chính"
        char ma_phe_duyet UK "Mã phê duyệt - Auto"
        date ngay_tao "Ngày tạo đơn"
        int de_xuat_mua_id FK "FK - Đề xuất gốc"
        char ma_de_xuat "Computed - Mã đề xuất"
        char ten_de_xuat "Tiêu đề"
        date ngay_de_xuat "Ngày đề xuất"
        int nguoi_de_xuat_id FK "FK - Người đề xuất"
        int phong_ban_id FK "FK - Phòng ban"
        float tong_gia_tri "Tổng giá trị"
        selection don_vi_tien_te "vnd/usd"
        text ly_do "Lý do đề xuất"
        html mo_ta "Mô tả chi tiết"
        date ngay_du_kien_nhan "Ngày dự kiến nhận"
        selection state "draft/approved/rejected/done/cancelled"
        int nguoi_phe_duyet_id FK "FK - Người phê duyệt"
        date ngay_phe_duyet "Ngày phê duyệt"
        text ghi_chu_phe_duyet "Ghi chú phê duyệt"
        int tk_tai_san_id FK "FK - TK Tài sản 211"
        int tk_nguon_von_id FK "FK - TK Nguồn vốn 112"
        int journal_id FK "FK - Sổ nhật ký"
        int but_toan_id FK "FK - Bút toán tạo"
        int tai_san_count "Computed - Số tài sản"
    }

    phe_duyet_mua_tai_san_line {
        int id PK "Khóa chính"
        int phe_duyet_id FK "FK - Đơn phê duyệt cha"
        char ten_thiet_bi "Tên thiết bị"
        int danh_muc_ts_id FK "FK - Danh mục"
        text mo_ta "Mô tả"
        text thong_so_ky_thuat "Thông số kỹ thuật"
        int so_luong "Số lượng"
        char don_vi_tinh "Đơn vị tính"
        float don_gia "Đơn giá"
        float thanh_tien "Computed - Thành tiền"
        selection pp_khau_hao "Phương pháp khấu hao"
        int thoi_gian_su_dung "Thời gian sử dụng (năm)"
        float ty_le_khau_hao "Tỷ lệ khấu hao"
        char nha_cung_cap "Nhà cung cấp"
    }

    khau_hao_tai_san {
        int id PK "Khóa chính"
        int tai_san_id FK "FK - Tài sản"
        int phe_duyet_mua_id FK "FK - Phê duyệt mua"
        date ngay_bat_dau "Ngày bắt đầu khấu hao"
        float gia_tri_ban_dau "Giá trị ban đầu"
        int thoi_gian_khau_hao "Thời gian khấu hao (năm)"
        float ty_le_khau_hao "Tỷ lệ khấu hao %/năm"
        selection phuong_phap "straight-line/degressive/none"
        int so_nam_khau_hao "Số năm khấu hao"
        float gia_tri_khau_hao_hang_nam "Computed - Khấu hao/năm"
        float tong_gia_tri_khau_hao "Computed - Tổng đã khấu hao"
        float gia_tri_con_lai "Computed - Giá trị còn lại"
        selection trang_thai "dang_khau_hao/tam_dung/hoan_thanh"
    }

    lich_khau_hao {
        int id PK "Khóa chính"
        int khau_hao_id FK "FK - Bản ghi khấu hao cha"
        int nam "Năm thứ mấy"
        date ngay_khau_hao "Ngày khấu hao"
        float gia_tri_khau_hao "Giá trị khấu hao kỳ"
        boolean da_ghi_nhan "Đã ghi nhận kế toán"
    }

    but_toan {
        int id PK "Khóa chính"
        char so_but_toan UK "Số bút toán - Auto"
        date ngay_but_toan "Ngày bút toán"
        text mo_ta "Mô tả nội dung"
        int khau_hao_id FK "FK - Khấu hao liên quan"
        int tai_khoan_no_id FK "FK - TK Nợ"
        int tai_khoan_co_id FK "FK - TK Có"
        float so_tien "Số tiền"
        selection trang_thai "draft/posted"
    }

    tai_khoan_quan_tri {
        int id PK "Khóa chính"
        char ten_tai_khoan "Tên tài khoản"
        char ma_tai_khoan "Mã tài khoản"
        int phong_ban_id FK "FK - Phòng ban"
        int phe_duyet_mua_id FK "FK - Phê duyệt mua"
        date ngay_ghi_nhan "Ngày ghi nhận"
        selection loai_giao_dich "mua_tai_san/thanh_ly/khau_hao/khac"
        text mo_ta "Mô tả"
        float so_tien "Số tiền"
        selection don_vi_tien_te "vnd/usd"
        float tong_chi_phi_khau_hao "Computed - Tổng chi phí"
        float chi_phi_thang_nay "Computed - Chi phí tháng"
    }

    bao_cao_tai_chinh {
        int id PK "Khóa chính"
        char name "Tên báo cáo"
        int thang "Tháng báo cáo"
        int nam "Năm báo cáo"
        selection trang_thai "draft/in_progress/completed/cancelled"
        float doanh_thu "Doanh thu"
        float tong_chi_phi "Computed - Tổng chi phí"
        float loi_nhuan "Computed - Lợi nhuận"
        float ty_le_loi_nhuan "Computed - Tỷ lệ %"
        float chi_phi_khau_hao "Chi phí khấu hao"
        float chi_phi_luong "Chi phí lương"
        float chi_phi_van_phong "Chi phí văn phòng"
        float chi_phi_marketing "Chi phí marketing"
        float chi_phi_dien_nuoc "Chi phí điện nước"
        float chi_phi_khac "Chi phí khác"
        datetime ngay_tao "Ngày tạo"
        datetime ngay_hoan_thanh "Ngày hoàn thành"
        int nguoi_tao_id FK "FK - Người tạo"
        int nguoi_xu_ly_id FK "FK - Người xử lý"
    }

    %% RELATIONSHIPS
    phe_duyet_mua_tai_san ||--o{ phe_duyet_mua_tai_san_line : "1-N"
    phe_duyet_mua_tai_san ||--o{ tai_khoan_quan_tri : "1-N"
    
    khau_hao_tai_san ||--o{ lich_khau_hao : "1-N"
    khau_hao_tai_san ||--o{ but_toan : "1-N"
```

---

# HÌNH 3.5: SƠ ĐỒ LUỒNG TỔNG QUAN HỆ THỐNG

```mermaid
flowchart TB
    subgraph PHASE1["📋 GIAI ĐOẠN 1: ĐỀ XUẤT MUA"]
        A1["👤 Nhân viên<br/>tạo đề xuất mua"] --> A2["📝 Thêm chi tiết<br/>thiết bị cần mua"]
        A2 --> A3["📤 Gửi đề xuất<br/>chờ phê duyệt"]
    end
    
    subgraph PHASE2["✅ GIAI ĐOẠN 2: PHÊ DUYỆT"]
        B1["📬 Tự động tạo<br/>đơn phê duyệt"] --> B2["👔 Quản lý TC<br/>xem xét"]
        B2 --> B3{{"Quyết định?"}}
        B3 -->|"Phê duyệt"| B4["✅ Cấu hình<br/>tài khoản kế toán"]
        B3 -->|"Từ chối"| B5["❌ Ghi lý do<br/>từ chối"]
    end
    
    subgraph PHASE3["📦 GIAI ĐOẠN 3: TẠO TÀI SẢN"]
        C1["🔄 Tự động tạo<br/>tài sản mới"] --> C2["📊 Tạo lịch<br/>khấu hao"]
        C2 --> C3["📝 Ghi bút toán<br/>Nợ 211 / Có 112"]
    end
    
    subgraph PHASE4["🔧 GIAI ĐOẠN 4: SỬ DỤNG"]
        D1["📍 Phân bổ<br/>cho phòng ban"] --> D2["👥 Gán nhân viên<br/>sử dụng"]
        D2 --> D3["🔄 Mượn/Trả<br/>nếu cần"]
        D3 --> D4["📋 Kiểm kê<br/>định kỳ"]
        D4 --> D5["🔀 Luân chuyển<br/>nếu cần"]
    end
    
    subgraph PHASE5["💰 GIAI ĐOẠN 5: KHẤU HAO"]
        E1["📅 Khấu hao<br/>định kỳ"] --> E2["📉 Cập nhật<br/>giá trị"]
        E2 --> E3["📝 Ghi bút toán<br/>Nợ 642 / Có 214"]
    end
    
    subgraph PHASE6["🗑️ GIAI ĐOẠN 6: THANH LÝ"]
        F1["📝 Tạo phiếu<br/>thanh lý"] --> F2{{"Hành động?"}}
        F2 -->|"Bán"| F3["💵 Ghi nhận<br/>giá bán"]
        F2 -->|"Tiêu hủy"| F4["🗑️ Ghi nhận<br/>tiêu hủy"]
        F3 --> F5["✅ Hoàn tất<br/>thanh lý"]
        F4 --> F5
    end
    
    A3 --> B1
    B4 --> C1
    B5 --> A1
    C3 --> D1
    D2 --> E1
    E2 --> F1

    classDef phase1 fill:#e3f2fd,stroke:#1565c0
    classDef phase2 fill:#f3e5f5,stroke:#7b1fa2
    classDef phase3 fill:#e8f5e9,stroke:#2e7d32
    classDef phase4 fill:#fff3e0,stroke:#ef6c00
    classDef phase5 fill:#fce4ec,stroke:#c2185b
    classDef phase6 fill:#f5f5f5,stroke:#616161
    
    class A1,A2,A3 phase1
    class B1,B2,B3,B4,B5 phase2
    class C1,C2,C3 phase3
    class D1,D2,D3,D4,D5 phase4
    class E1,E2,E3 phase5
    class F1,F2,F3,F4,F5 phase6
```

---

# HÌNH 3.6: SƠ ĐỒ LUỒNG ĐỀ XUẤT MUA TÀI SẢN

```mermaid
flowchart TD
    START(("🚀 Bắt đầu")) --> A["👤 Nhân viên truy cập<br/>menu Đề xuất mua tài sản"]
    
    A --> B["📝 Tạo đề xuất mới<br/>State: DRAFT"]
    
    B --> C["✏️ Nhập thông tin cơ bản:<br/>- Tiêu đề đề xuất<br/>- Lý do mua<br/>- Phòng ban<br/>- Ngày dự kiến nhận"]
    
    C --> D["➕ Thêm chi tiết thiết bị:<br/>- Tên thiết bị<br/>- Danh mục<br/>- Số lượng<br/>- Đơn giá<br/>- Thông số kỹ thuật<br/>- Phương pháp khấu hao"]
    
    D --> E["💰 Hệ thống tự động<br/>tính tổng giá trị"]
    
    E --> F["📎 Đính kèm file<br/>(Báo giá, hình ảnh...)"]
    
    F --> G["💾 Lưu đề xuất"]
    
    G --> H{{"Gửi đề xuất?"}}
    
    H -->|"Chưa"| I["📋 Giữ trạng thái<br/>DRAFT"]
    I --> G
    
    H -->|"Có"| J["📤 Action: Gửi đề xuất<br/>action_submit()"]
    
    J --> K["🔄 Validate dữ liệu:<br/>- Có chi tiết thiết bị?<br/>- Tổng giá trị > 0?"]
    
    K --> L{{"Valid?"}}
    
    L -->|"Không"| M["⚠️ Thông báo lỗi<br/>ValidationError"]
    M --> C
    
    L -->|"Có"| N["📬 Tạo đơn phê duyệt<br/>tại module Tài chính"]
    
    N --> O["🔗 Liên kết phe_duyet_id"]
    
    O --> P["📝 Cập nhật state:<br/>WAITING_APPROVAL"]
    
    P --> Q["📧 Gửi thông báo<br/>cho Quản lý TC"]
    
    Q --> R(("⏳ Chờ phê duyệt"))

    classDef startEnd fill:#4caf50,stroke:#2e7d32,color:white
    classDef process fill:#e3f2fd,stroke:#1565c0
    classDef decision fill:#fff3e0,stroke:#ef6c00
    classDef action fill:#f3e5f5,stroke:#7b1fa2
    classDef error fill:#ffebee,stroke:#c62828
    
    class START,R startEnd
    class A,B,C,D,E,F,G,I,N,O,P,Q process
    class H,L decision
    class J,K action
    class M error
```

---

# HÌNH 3.7: SƠ ĐỒ VÒNG ĐỜI TÀI SẢN

```mermaid
stateDiagram-v2
    [*] --> CHUA_PHAN_BO: Tạo tài sản mới
    
    state "📦 CHƯA PHÂN BỔ" as CHUA_PHAN_BO {
        state "Tài sản mới tạo" as new_asset
        state "Chờ phân bổ" as waiting
        new_asset --> waiting
    }
    
    CHUA_PHAN_BO --> DA_PHAN_BO: Phân bổ cho phòng ban
    
    state "✅ ĐÃ PHÂN BỔ" as DA_PHAN_BO {
        state "Đang sử dụng" as in_use
        state "Tạm dừng sử dụng" as not_in_use
        state "Đang mượn" as borrowed
        state "Bảo dưỡng" as maintenance
        
        in_use --> not_in_use: Ngừng sử dụng
        not_in_use --> in_use: Sử dụng lại
        in_use --> borrowed: Cho mượn
        borrowed --> in_use: Trả lại
        in_use --> maintenance: Bảo dưỡng
        maintenance --> in_use: Hoàn thành
    }
    
    DA_PHAN_BO --> CHUA_PHAN_BO: Thu hồi
    DA_PHAN_BO --> DA_PHAN_BO: Luân chuyển
    
    state "🗑️ ĐÃ THANH LÝ" as DA_THANH_LY {
        state "Đã bán" as sold
        state "Đã tiêu hủy" as destroyed
    }
    
    CHUA_PHAN_BO --> DA_THANH_LY: Thanh lý (Bán/Hủy)
    DA_PHAN_BO --> DA_THANH_LY: Thu hồi + Thanh lý
    
    DA_THANH_LY --> [*]
    
    note right of CHUA_PHAN_BO
        Tài sản chưa gán
        cho phòng ban nào
    end note
    
    note right of DA_PHAN_BO
        Tài sản đang được
        sử dụng hoặc quản lý
        bởi phòng ban
    end note
    
    note right of DA_THANH_LY
        Trạng thái cuối cùng
        Không thể phục hồi
    end note
```

---

# HÌNH 3.8: SƠ ĐỒ LUỒNG MƯỢN TRẢ TÀI SẢN

```mermaid
flowchart TD
    subgraph STEP1["📝 BƯỚC 1: TẠO ĐƠN MƯỢN"]
        A["👤 Nhân viên<br/>cần mượn tài sản"] --> B["📋 Tạo Đơn mượn tài sản<br/>don_muon_tai_san"]
        B --> C["✏️ Điền thông tin:<br/>- Phòng ban cho mượn<br/>- Thời gian mượn/trả<br/>- Lý do mượn"]
        C --> D["➕ Chọn tài sản mượn<br/>từ danh sách phân bổ"]
        D --> E["💾 Lưu đơn (NHÁP)"]
        E --> F["📤 Gửi yêu cầu mượn<br/>action_submit()"]
    end
    
    subgraph STEP2["✅ BƯỚC 2: PHÊ DUYỆT"]
        G["👔 Quản lý nhận<br/>yêu cầu mượn"] --> H{{"Xem xét<br/>đơn mượn"}}
        H -->|"Đủ điều kiện"| I["✅ Phê duyệt<br/>action_approve()"]
        H -->|"Không đủ"| J["❌ Từ chối<br/>action_reject()"]
    end
    
    subgraph STEP3["📦 BƯỚC 3: XỬ LÝ MƯỢN"]
        K["🔄 Tự động tạo<br/>Phiếu mượn trả<br/>muon_tra_tai_san"] --> L["📍 Cập nhật trạng thái<br/>tài sản: ĐANG MƯỢN"]
        L --> M["👤 Giao tài sản<br/>cho người mượn"]
        M --> N["📅 Theo dõi<br/>thời hạn trả"]
    end
    
    subgraph STEP4["🔙 BƯỚC 4: TRẢ TÀI SẢN"]
        O["⏰ Đến hạn trả"] --> P["👤 Nhân viên<br/>trả tài sản"]
        P --> Q["🔍 Kiểm tra<br/>tình trạng tài sản"]
        Q --> R["✏️ Ghi nhận<br/>tình trạng sau trả"]
        R --> S["✅ Xác nhận trả<br/>action_return()"]
        S --> T["🔄 Cập nhật trạng thái<br/>tài sản: BÌNH THƯỜNG"]
    end
    
    subgraph ALERT["⚠️ XỬ LÝ QUÁ HẠN"]
        U["⏰ Quá hạn trả"] --> V["📧 Gửi thông báo<br/>nhắc nhở"]
        V --> W["📋 Ghi nhận<br/>vi phạm (nếu có)"]
    end
    
    F --> G
    I --> K
    J --> E
    N --> O
    N --> U
    W --> P

    classDef step1 fill:#e3f2fd,stroke:#1565c0
    classDef step2 fill:#f3e5f5,stroke:#7b1fa2
    classDef step3 fill:#e8f5e9,stroke:#2e7d32
    classDef step4 fill:#fff3e0,stroke:#ef6c00
    classDef alert fill:#ffebee,stroke:#c62828
    
    class A,B,C,D,E,F step1
    class G,H,I,J step2
    class K,L,M,N step3
    class O,P,Q,R,S,T step4
    class U,V,W alert
```

---

# HÌNH 3.9: SƠ ĐỒ LUỒNG KIỂM KÊ TÀI SẢN

```mermaid
flowchart TD
    START(("🚀 Bắt đầu<br/>kiểm kê")) --> A["📋 Tạo phiếu kiểm kê<br/>kiem_ke_tai_san"]
    
    A --> B["✏️ Nhập thông tin:<br/>- Mã phiếu<br/>- Tên phiếu<br/>- Nhân viên kiểm kê"]
    
    B --> C["🏢 Chọn phòng ban<br/>cần kiểm kê"]
    
    C --> D["🔄 Hệ thống tự động<br/>load danh sách tài sản<br/>của phòng ban"]
    
    D --> E["📋 Hiển thị danh sách<br/>tài sản chưa kiểm kê"]
    
    E --> F["➕ Thêm tài sản<br/>vào phiếu kiểm kê"]
    
    F --> G["🔍 Kiểm kê từng tài sản"]
    
    G --> H["✏️ Ghi nhận kết quả:<br/>- Số lượng thực tế<br/>- Tình trạng (Tốt/Hỏng/Mất)<br/>- Ghi chú"]
    
    H --> I{{"Còn tài sản<br/>cần kiểm kê?"}}
    
    I -->|"Có"| G
    
    I -->|"Không"| J["✅ Đánh dấu<br/>hoàn thành kiểm kê"]
    
    J --> K["📊 Tự động cập nhật<br/>trạng thái phiếu"]
    
    K --> L{{"Có tài sản<br/>bị mất/hỏng?"}}
    
    L -->|"Có"| M["⚠️ Tạo cảnh báo<br/>cập nhật tình trạng"]
    
    M --> N["📝 Cập nhật tình trạng<br/>tại phan_bo_tai_san"]
    
    L -->|"Không"| O["✅ Phiếu hoàn thành<br/>Tình trạng: Đã kiểm kê"]
    
    N --> O
    
    O --> P["📈 Tạo báo cáo<br/>kiểm kê"]
    
    P --> END(("✅ Kết thúc"))

    classDef startEnd fill:#4caf50,stroke:#2e7d32,color:white
    classDef process fill:#e3f2fd,stroke:#1565c0
    classDef decision fill:#fff3e0,stroke:#ef6c00
    classDef warning fill:#ffebee,stroke:#c62828
    classDef success fill:#e8f5e9,stroke:#2e7d32
    
    class START,END startEnd
    class A,B,C,D,E,F,G,H,K,P process
    class I,L decision
    class M,N warning
    class J,O success
```

---

# HÌNH 3.10: SƠ ĐỒ LUỒNG KHẤU HAO TÀI SẢN

```mermaid
flowchart TD
    subgraph INPUT["📥 KHỞI TẠO KHẤU HAO"]
        A["📦 Tài sản mới<br/>được tạo"] --> B{{"Có thông tin<br/>khấu hao?"}}
        B -->|"Có"| C["📊 Tạo bản ghi<br/>khau_hao_tai_san"]
        B -->|"Không"| D["⏭️ Bỏ qua<br/>không khấu hao"]
    end
    
    subgraph CONFIG["⚙️ CẤU HÌNH KHẤU HAO"]
        C --> E["✏️ Nhập thông tin:<br/>- Ngày bắt đầu<br/>- Số năm khấu hao<br/>- Phương pháp"]
        
        E --> F{{"Phương pháp?"}}
        
        F -->|"Tuyến tính"| G["📐 Tính khấu hao:<br/>KH = Giá trị / Số năm"]
        
        F -->|"Giảm dần"| H["📉 Tính khấu hao:<br/>KH = Giá trị × Tỷ lệ%"]
        
        F -->|"Không"| D
    end
    
    subgraph SCHEDULE["📅 TẠO LỊCH KHẤU HAO"]
        G --> I["🔄 _tao_lich_khau_hao()"]
        H --> I
        
        I --> J["📋 Tạo lịch chi tiết<br/>lich_khau_hao cho từng năm"]
        
        J --> K["📊 Hiển thị lịch:<br/>- Năm<br/>- Ngày khấu hao<br/>- Giá trị khấu hao"]
    end
    
    subgraph EXECUTE["💰 THỰC HIỆN KHẤU HAO"]
        K --> L["⏰ Đến ngày<br/>khấu hao"]
        
        L --> M["📝 Ghi nhận khấu hao<br/>lich_su_khau_hao"]
        
        M --> N["💵 Cập nhật giá trị:<br/>gia_tri_hien_tai -= so_tien"]
        
        N --> O["📝 Tạo bút toán:<br/>Nợ 642 / Có 214"]
        
        O --> P{{"Còn kỳ<br/>khấu hao?"}}
        
        P -->|"Có"| L
        
        P -->|"Không"| Q["✅ Hoàn thành<br/>khấu hao"]
    end
    
    subgraph RESULT["📊 KẾT QUẢ"]
        Q --> R["📈 Giá trị còn lại = 0<br/>hoặc giá trị thanh lý"]
        
        R --> S["📋 Báo cáo tổng hợp<br/>khấu hao"]
    end

    classDef input fill:#e3f2fd,stroke:#1565c0
    classDef config fill:#f3e5f5,stroke:#7b1fa2
    classDef schedule fill:#fff3e0,stroke:#ef6c00
    classDef execute fill:#e8f5e9,stroke:#2e7d32
    classDef result fill:#fce4ec,stroke:#c2185b
    
    class A,B,C,D input
    class E,F,G,H config
    class I,J,K schedule
    class L,M,N,O,P,Q execute
    class R,S result
```

---

# HÌNH 3.11: SƠ ĐỒ LUỒNG THANH LÝ TÀI SẢN

```mermaid
flowchart TD
    START(("🚀 Bắt đầu<br/>thanh lý")) --> A["📦 Chọn tài sản<br/>cần thanh lý"]
    
    A --> B{{"Tài sản đã<br/>thanh lý trước đó?"}}
    
    B -->|"Rồi"| C["⚠️ ValidationError:<br/>Tài sản đã thanh lý!"]
    C --> END1(("❌ Kết thúc"))
    
    B -->|"Chưa"| D{{"Tài sản đang<br/>được phân bổ?"}}
    
    D -->|"Có"| E["🔄 Thu hồi phân bổ<br/>trước khi thanh lý"]
    
    D -->|"Không"| F["📋 Tạo phiếu thanh lý<br/>thanh_ly_tai_san"]
    
    E --> F
    
    F --> G["✏️ Nhập thông tin:<br/>- Mã thanh lý<br/>- Người thực hiện<br/>- Lý do thanh lý"]
    
    G --> H{{"Chọn hành động?"}}
    
    H -->|"Bán"| I["💵 Nhập giá bán<br/>(>= 0)"]
    
    I --> J["📝 Ghi nhận:<br/>- Giá bán<br/>- Giá gốc (computed)"]
    
    H -->|"Tiêu hủy"| K["🗑️ Giá bán = 0<br/>Ghi lý do tiêu hủy"]
    
    J --> L["✅ Xác nhận thanh lý"]
    K --> L
    
    L --> M["🔄 Cập nhật trạng thái<br/>tài sản: ĐÃ THANH LÝ"]
    
    M --> N["📊 Ghi nhận tài chính<br/>(nếu có bút toán)"]
    
    N --> O["📋 Tạo báo cáo<br/>thanh lý tài sản"]
    
    O --> END2(("✅ Hoàn thành"))

    classDef startEnd fill:#4caf50,stroke:#2e7d32,color:white
    classDef error fill:#ffebee,stroke:#c62828
    classDef process fill:#e3f2fd,stroke:#1565c0
    classDef decision fill:#fff3e0,stroke:#ef6c00
    classDef action fill:#f3e5f5,stroke:#7b1fa2
    
    class START,END2 startEnd
    class C,END1 error
    class A,E,F,G,I,J,K,M,N,O process
    class B,D,H decision
    class L action
```

---

# HÌNH 3.12: GIAO DIỆN DASHBOARD TỔNG QUAN TÀI SẢN

```mermaid
flowchart TB
    subgraph DASHBOARD["📊 DASHBOARD TỔNG QUAN TÀI SẢN"]
        subgraph KPI["📈 KPI CARDS"]
            direction LR
            K1["📦 TỔNG TÀI SẢN<br/>━━━━━━━━━━<br/>156<br/><small>+12 so với tháng trước</small>"]
            K2["✅ ĐANG SỬ DỤNG<br/>━━━━━━━━━━<br/>128<br/><small>82% tổng số</small>"]
            K3["⏸️ KHÔNG SỬ DỤNG<br/>━━━━━━━━━━<br/>18<br/><small>12% tổng số</small>"]
            K4["🗑️ ĐÃ THANH LÝ<br/>━━━━━━━━━━<br/>10<br/><small>Trong năm nay</small>"]
        end
        
        subgraph CHARTS["📊 BIỂU ĐỒ"]
            direction LR
            subgraph PIE["🥧 PHÂN BỔ THEO LOẠI"]
                P1["Máy tính 35%"]
                P2["Bàn ghế 25%"]
                P3["Thiết bị văn phòng 20%"]
                P4["Phương tiện 15%"]
                P5["Khác 5%"]
            end
            
            subgraph BAR["📊 PHÂN BỔ THEO PHÒNG BAN"]
                B1["Kỹ thuật: 45"]
                B2["Kinh doanh: 38"]
                B3["Nhân sự: 25"]
                B4["Tài chính: 22"]
                B5["Hành chính: 26"]
            end
        end
        
        subgraph TABLE["📋 TÀI SẢN GIÁ TRỊ CAO"]
            T1["#1 | Máy chủ Dell R740 | 250,000,000 VNĐ | Kỹ thuật"]
            T2["#2 | Ô tô Toyota | 850,000,000 VNĐ | Kinh doanh"]
            T3["#3 | Máy in Konica | 180,000,000 VNĐ | Hành chính"]
            T4["#4 | Laptop MacBook | 45,000,000 VNĐ | Kỹ thuật"]
            T5["#5 | Máy chiếu Epson | 35,000,000 VNĐ | Đào tạo"]
        end
        
        subgraph ALERTS["⚠️ CẢNH BÁO"]
            A1["🔴 5 tài sản quá hạn kiểm kê"]
            A2["🟡 3 đơn mượn chờ duyệt"]
            A3["🟢 2 đề xuất mua đã phê duyệt"]
        end
    end
    
    KPI --> CHARTS
    CHARTS --> TABLE
    TABLE --> ALERTS
```

---

# HÌNH 3.13: GIAO DIỆN FORM TÀI SẢN

```mermaid
flowchart TB
    subgraph FORM["📋 FORM TÀI SẢN - tai_san"]
        subgraph HEADER["🔝 HEADER"]
            direction LR
            H1["<b>Mã:</b> TS-00045"]
            H2["<b>Tên:</b> Laptop Dell XPS 15"]
            H3["🏷️ Trạng thái: ĐÃ PHÂN BỔ"]
        end
        
        subgraph BUTTONS["🔘 BUTTONS"]
            direction LR
            BTN1["📊 Khấu hao"]
            BTN2["📍 Phân bổ"]
            BTN3["📜 Lịch sử"]
            BTN4["🗑️ Thanh lý"]
        end
        
        subgraph TAB1["📑 TAB: THÔNG TIN CHUNG"]
            direction TB
            subgraph LEFT["Cột trái"]
                L1["<b>Mã tài sản:</b> TS-00045"]
                L2["<b>Tên tài sản:</b> Laptop Dell XPS 15"]
                L3["<b>Loại tài sản:</b> Máy tính"]
                L4["<b>Ngày mua:</b> 15/03/2025"]
                L5["<b>Đơn vị tính:</b> Chiếc"]
            end
            subgraph RIGHT["Cột phải"]
                R1["<b>Giá trị ban đầu:</b> 45,000,000 VNĐ"]
                R2["<b>Giá trị hiện tại:</b> 36,000,000 VNĐ"]
                R3["<b>📷 Hình ảnh</b>"]
                R4["<b>📎 File đính kèm:</b> warranty.pdf"]
            end
        end
        
        subgraph TAB2["📑 TAB: KHẤU HAO"]
            KH1["<b>Phương pháp:</b> Tuyến tính"]
            KH2["<b>Thời gian sử dụng:</b> 1 năm"]
            KH3["<b>Thời gian tối đa:</b> 5 năm"]
            KH4["<b>Tỷ lệ khấu hao:</b> 20%/năm"]
        end
        
        subgraph TAB3["📑 TAB: PHÂN BỔ"]
            PB1["| Phòng ban | Nhân viên | Ngày phân bổ | Trạng thái |"]
            PB2["| Kỹ thuật  | Nguyễn A | 20/03/2025  | Đang dùng  |"]
        end
        
        subgraph TAB4["📑 TAB: LỊCH SỬ"]
            LS1["📊 Lịch sử khấu hao"]
            LS2["📋 Lịch sử kiểm kê"]
            LS3["🔀 Lịch sử luân chuyển"]
            LS4["🔧 Lịch sử kỹ thuật"]
        end
    end
    
    HEADER --> BUTTONS
    BUTTONS --> TAB1
    TAB1 --> TAB2
    TAB2 --> TAB3
    TAB3 --> TAB4
```

---

# HÌNH 3.14: GIAO DIỆN FORM ĐỀ XUẤT MUA TÀI SẢN

```mermaid
flowchart TB
    subgraph FORM["📋 FORM ĐỀ XUẤT MUA TÀI SẢN"]
        subgraph HEADER["🔝 HEADER"]
            direction LR
            H1["<b>Mã:</b> DXMTS-00012"]
            H2["📅 Ngày: 25/01/2026"]
            H3["🏷️ Trạng thái: CHỜ PHÊ DUYỆT"]
        end
        
        subgraph BUTTONS["🔘 ACTION BUTTONS"]
            direction LR
            BTN1["📤 GỬI ĐỀ XUẤT"]
            BTN2["❌ HỦY"]
            BTN3["📋 XEM PHÊ DUYỆT"]
        end
        
        subgraph INFO["📝 THÔNG TIN ĐỀ XUẤT"]
            direction TB
            subgraph COL1[""]
                I1["<b>Tiêu đề:</b> Mua laptop cho phòng Kỹ thuật"]
                I2["<b>Người đề xuất:</b> Trần Văn B"]
                I3["<b>Phòng ban:</b> Phòng Kỹ thuật"]
            end
            subgraph COL2[""]
                I4["<b>Ngày dự kiến nhận:</b> 15/02/2026"]
                I5["<b>Đơn vị tiền tệ:</b> VNĐ"]
                I6["<b>💰 TỔNG GIÁ TRỊ:</b> 135,000,000"]
            end
        end
        
        subgraph LINES["📦 CHI TIẾT THIẾT BỊ"]
            LINE_HEADER["| # | Tên thiết bị | Danh mục | SL | Đơn giá | Thành tiền |"]
            LINE1["| 1 | Laptop Dell XPS 15 | Máy tính | 3 | 45,000,000 | 135,000,000 |"]
            LINE2["| ➕ Thêm dòng |"]
        end
        
        subgraph REASON["📝 LÝ DO VÀ MÔ TẢ"]
            R1["<b>Lý do đề xuất:</b>"]
            R2["Phòng Kỹ thuật cần bổ sung thêm laptop cho nhân viên mới..."]
            R3["<b>Mô tả chi tiết:</b> (Rich Text Editor)"]
        end
        
        subgraph ATTACH["📎 FILE ĐÍNH KÈM"]
            A1["📄 bao_gia_dell.pdf"]
            A2["🖼️ laptop_specs.png"]
            A3["➕ Thêm file"]
        end
    end
    
    HEADER --> BUTTONS
    BUTTONS --> INFO
    INFO --> LINES
    LINES --> REASON
    REASON --> ATTACH
```

---

# HÌNH 3.15: GIAO DIỆN DASHBOARD TÀI CHÍNH

```mermaid
flowchart TB
    subgraph DASHBOARD["📊 DASHBOARD TÀI CHÍNH"]
        subgraph APPROVAL["✅ SECTION: PHÊ DUYỆT MUA TÀI SẢN"]
            direction LR
            AP1["📋 TỔNG ĐƠN<br/>━━━━━━<br/>45"]
            AP2["⏳ CHỜ DUYỆT<br/>━━━━━━<br/>8"]
            AP3["✅ ĐÃ DUYỆT<br/>━━━━━━<br/>32"]
            AP4["❌ TỪ CHỐI<br/>━━━━━━<br/>5"]
        end
        
        subgraph DEPRECIATION["📉 SECTION: KHẤU HAO"]
            direction LR
            DP1["📦 TỔNG TÀI SẢN<br/>KHẤU HAO<br/>━━━━━━<br/>120"]
            DP2["🔄 ĐANG<br/>KHẤU HAO<br/>━━━━━━<br/>98"]
            DP3["✅ ĐÃ HOÀN<br/>THÀNH<br/>━━━━━━<br/>22"]
            DP4["💰 GIÁ TRỊ<br/>CÒN LẠI<br/>━━━━━━<br/>2.5 tỷ VNĐ"]
        end
        
        subgraph JOURNAL["📝 SECTION: BÚT TOÁN"]
            direction LR
            JN1["📋 TỔNG<br/>BÚT TOÁN<br/>━━━━━━<br/>256"]
            JN2["📝 NHÁP<br/>━━━━━━<br/>12"]
            JN3["✅ ĐÃ VÀO SỔ<br/>━━━━━━<br/>244"]
            JN4["💵 TỔNG GIÁ TRỊ<br/>━━━━━━<br/>5.8 tỷ VNĐ"]
        end
        
        subgraph CHARTS["📊 BIỂU ĐỒ"]
            direction LR
            subgraph TREND["📈 XU HƯỚNG KHẤU HAO"]
                TR1["Tháng 1: 120tr"]
                TR2["Tháng 2: 135tr"]
                TR3["Tháng 3: 142tr"]
            end
            subgraph EXPENSE["🥧 PHÂN BỔ CHI PHÍ"]
                EX1["Khấu hao: 45%"]
                EX2["Mua mới: 35%"]
                EX3["Bảo trì: 15%"]
                EX4["Khác: 5%"]
            end
        end
        
        subgraph RECENT["📋 ĐƠN PHÊ DUYỆT GẦN ĐÂY"]
            RC1["| PDMTS-00045 | Mua máy in | 25/01/2026 | Chờ duyệt |"]
            RC2["| PDMTS-00044 | Mua laptop  | 23/01/2026 | Đã duyệt  |"]
            RC3["| PDMTS-00043 | Mua bàn ghế | 20/01/2026 | Đã duyệt  |"]
        end
    end
    
    APPROVAL --> DEPRECIATION
    DEPRECIATION --> JOURNAL
    JOURNAL --> CHARTS
    CHARTS --> RECENT
```

---

# HÌNH 3.16: GIAO DIỆN FORM PHÊ DUYỆT MUA TÀI SẢN

```mermaid
flowchart TB
    subgraph FORM["📋 FORM PHÊ DUYỆT MUA TÀI SẢN"]
        subgraph HEADER["🔝 HEADER"]
            direction LR
            H1["<b>Mã phê duyệt:</b> PDMTS-00045"]
            H2["📅 Ngày: 25/01/2026"]
            H3["🏷️ Trạng thái: CHỜ XỬ LÝ"]
        end
        
        subgraph BUTTONS["🔘 ACTION BUTTONS"]
            direction LR
            BTN1["✅ PHÊ DUYỆT"]
            BTN2["❌ TỪ CHỐI"]
            BTN3["📦 XEM TÀI SẢN (0)"]
        end
        
        subgraph PROPOSAL_INFO["📝 THÔNG TIN ĐỀ XUẤT (Readonly)"]
            direction TB
            subgraph COL1[""]
                P1["<b>Mã đề xuất:</b> DXMTS-00012"]
                P2["<b>Tiêu đề:</b> Mua laptop cho phòng Kỹ thuật"]
                P3["<b>Người đề xuất:</b> Trần Văn B"]
            end
            subgraph COL2[""]
                P4["<b>Phòng ban:</b> Phòng Kỹ thuật"]
                P5["<b>Ngày đề xuất:</b> 24/01/2026"]
                P6["<b>💰 Tổng giá trị:</b> 135,000,000 VNĐ"]
            end
        end
        
        subgraph LINES["📦 CHI TIẾT THIẾT BỊ (Readonly)"]
            LINE_H["| Thiết bị | Danh mục | SL | Đơn giá | PP Khấu hao | Thời gian |"]
            LINE1["| Laptop Dell XPS | Máy tính | 3 | 45,000,000 | Tuyến tính | 5 năm |"]
        end
        
        subgraph ACCOUNT_CONFIG["⚙️ CẤU HÌNH TÀI KHOẢN"]
            AC1["<b>TK Tài sản cố định:</b> 211 - TSCĐ hữu hình"]
            AC2["<b>TK Nguồn vốn:</b> 1121 - Tiền gửi ngân hàng"]
            AC3["<b>Sổ nhật ký:</b> Sổ mua hàng"]
        end
        
        subgraph APPROVAL_INFO["✅ THÔNG TIN PHÊ DUYỆT"]
            AI1["<b>Người phê duyệt:</b> (Tự động điền)"]
            AI2["<b>Ngày phê duyệt:</b> (Tự động điền)"]
            AI3["<b>Ghi chú phê duyệt:</b> (Nhập nếu cần)"]
        end
    end
    
    HEADER --> BUTTONS
    BUTTONS --> PROPOSAL_INFO
    PROPOSAL_INFO --> LINES
    LINES --> ACCOUNT_CONFIG
    ACCOUNT_CONFIG --> APPROVAL_INFO
```

---

# HÌNH 3.17: MẪU BÁO CÁO TÀI CHÍNH

```mermaid
flowchart TB
    subgraph REPORT["📊 BÁO CÁO TÀI CHÍNH THÁNG 01/2026"]
        subgraph HEADER["🏢 HEADER BÁO CÁO"]
            H1["<b>CÔNG TY TNHH ABC</b>"]
            H2["━━━━━━━━━━━━━━━━━━━━"]
            H3["<b>BÁO CÁO TÀI CHÍNH</b>"]
            H4["Kỳ báo cáo: Tháng 01/2026"]
        end
        
        subgraph SUMMARY["📈 TỔNG HỢP"]
            direction LR
            S1["💰 DOANH THU<br/>━━━━━━━━<br/>500,000,000 VNĐ"]
            S2["💸 TỔNG CHI PHÍ<br/>━━━━━━━━<br/>380,000,000 VNĐ"]
            S3["📊 LỢI NHUẬN<br/>━━━━━━━━<br/>120,000,000 VNĐ"]
            S4["📈 TỶ LỆ LN<br/>━━━━━━━━<br/>24%"]
        end
        
        subgraph DETAIL["📋 CHI TIẾT CHI PHÍ"]
            D1["| Loại chi phí | Số tiền | Tỷ lệ |"]
            D2["| Chi phí khấu hao | 45,000,000 | 11.8% |"]
            D3["| Chi phí lương | 200,000,000 | 52.6% |"]
            D4["| Chi phí văn phòng | 35,000,000 | 9.2% |"]
            D5["| Chi phí marketing | 50,000,000 | 13.2% |"]
            D6["| Chi phí điện nước | 20,000,000 | 5.3% |"]
            D7["| Chi phí khác | 30,000,000 | 7.9% |"]
            D8["| <b>TỔNG CỘNG</b> | <b>380,000,000</b> | <b>100%</b> |"]
        end
        
        subgraph CHART["📊 BIỂU ĐỒ PHÂN BỔ CHI PHÍ"]
            C1["🥧 Pie Chart hiển thị % từng loại chi phí"]
        end
        
        subgraph FOOTER["📝 FOOTER"]
            F1["Ngày lập: 28/01/2026"]
            F2["Người lập: Nguyễn Văn A"]
            F3["━━━━━━━━━━━━━━━━━"]
            F4["Chữ ký: _______________"]
        end
    end
    
    HEADER --> SUMMARY
    SUMMARY --> DETAIL
    DETAIL --> CHART
    CHART --> FOOTER
```

---

# HÌNH 3.18: SƠ ĐỒ TÍCH HỢP 2 MODULE

```mermaid
flowchart TB
    subgraph ASSET_MODULE["📦 MODULE QUẢN LÝ TÀI SẢN<br/>(quan_ly_tai_san)"]
        A1["📝 de_xuat_mua_tai_san<br/>Đề xuất mua tài sản"]
        A2["📦 tai_san<br/>Tài sản"]
        A3["📍 phan_bo_tai_san<br/>Phân bổ tài sản"]
        A4["📊 lich_su_khau_hao<br/>Lịch sử khấu hao"]
    end
    
    subgraph FINANCE_MODULE["💰 MODULE QUẢN LÝ TÀI CHÍNH<br/>(quan_ly_tai_chinh)"]
        F1["✅ phe_duyet_mua_tai_san<br/>Phê duyệt mua"]
        F2["📉 khau_hao_tai_san<br/>Khấu hao tài sản"]
        F3["📝 but_toan<br/>Bút toán kế toán"]
        F4["📊 tai_khoan_quan_tri<br/>Tài khoản quản trị"]
    end
    
    subgraph INTEGRATION["🔗 ĐIỂM TÍCH HỢP"]
        I1["1️⃣ Gửi đề xuất → Tạo đơn phê duyệt"]
        I2["2️⃣ Phê duyệt → Tạo tài sản tự động"]
        I3["3️⃣ Tạo tài sản → Tạo lịch khấu hao"]
        I4["4️⃣ Đồng bộ trạng thái hai chiều"]
    end
    
    A1 -->|"action_submit()"| I1
    I1 -->|"Tự động tạo"| F1
    
    F1 -->|"action_approve()"| I2
    I2 -->|"_tao_tai_san()"| A2
    
    I2 -->|"Đồng thời"| I3
    I3 -->|"_create_khau_hao()"| F2
    
    F2 -->|"_tao_but_toan()"| F3
    F2 -->|"Ghi nhận"| F4
    
    F1 <-->|"Đồng bộ state"| A1
    F2 -->|"Cập nhật giá trị"| A4
    
    classDef assetStyle fill:#e8f5e9,stroke:#2e7d32
    classDef financeStyle fill:#e3f2fd,stroke:#1565c0
    classDef integrationStyle fill:#fff3e0,stroke:#ef6c00
    
    class A1,A2,A3,A4 assetStyle
    class F1,F2,F3,F4 financeStyle
    class I1,I2,I3,I4 integrationStyle
```

---

# HÌNH 3.19: SEQUENCE DIAGRAM - LUỒNG TÍCH HỢP MUA TÀI SẢN

```mermaid
sequenceDiagram
    autonumber
    participant NV as 👤 Nhân viên
    participant QLTS as 📦 Module Tài sản
    participant QLTC as 💰 Module Tài chính
    participant DB as 💾 Database
    
    rect rgb(232, 245, 233)
        Note over NV,QLTS: GIAI ĐOẠN 1: TẠO ĐỀ XUẤT
        NV->>QLTS: Tạo đề xuất mua tài sản
        QLTS->>QLTS: Nhập chi tiết thiết bị
        QLTS->>QLTS: Tính tổng giá trị
        QLTS->>DB: Lưu de_xuat_mua_tai_san
        DB-->>QLTS: OK - state: draft
    end
    
    rect rgb(227, 242, 253)
        Note over QLTS,QLTC: GIAI ĐOẠN 2: GỬI VÀ TẠO PHÊ DUYỆT
        NV->>QLTS: action_submit()
        QLTS->>QLTS: Validate dữ liệu
        QLTS->>QLTC: _create_phe_duyet()
        QLTC->>DB: Tạo phe_duyet_mua_tai_san
        DB-->>QLTC: OK - state: draft
        QLTC-->>QLTS: phe_duyet_id
        QLTS->>DB: Update state: waiting_approval
        QLTS-->>NV: Thông báo đã gửi
    end
    
    rect rgb(243, 229, 245)
        Note over QLTC: GIAI ĐOẠN 3: PHÊ DUYỆT
        QLTC->>QLTC: Quản lý TC xem xét
        QLTC->>QLTC: Cấu hình TK kế toán
        QLTC->>QLTC: action_approve()
    end
    
    rect rgb(255, 243, 224)
        Note over QLTS,DB: GIAI ĐOẠN 4: TẠO TÀI SẢN
        QLTC->>QLTS: _tao_tai_san_tu_phe_duyet()
        loop Mỗi dòng thiết bị
            QLTS->>DB: Tạo tai_san mới
            DB-->>QLTS: tai_san_id
        end
        QLTS-->>QLTC: tai_san_ids
    end
    
    rect rgb(252, 228, 236)
        Note over QLTC,DB: GIAI ĐOẠN 5: GHI NHẬN TÀI CHÍNH
        QLTC->>DB: Tạo khau_hao_tai_san
        QLTC->>DB: Tạo lich_khau_hao
        QLTC->>DB: Tạo but_toan (Nợ 211/Có 112)
        QLTC->>DB: Tạo tai_khoan_quan_tri
    end
    
    rect rgb(232, 245, 233)
        Note over QLTS,NV: GIAI ĐOẠN 6: CẬP NHẬT TRẠNG THÁI
        QLTC->>QLTS: _on_approval_approved()
        QLTS->>DB: Update de_xuat state: approved
        QLTS->>NV: Thông báo phê duyệt thành công
        QLTS-->>NV: Link đến tài sản đã tạo
    end
```

---

# BẢNG TÓM TẮT 19 HÌNH ẢNH

| STT | Mã hình | Tên hình | Loại sơ đồ | Mô tả |
|-----|---------|----------|------------|-------|
| 1 | HÌNH 3.1 | Kiến trúc tổng thể hệ thống | Flowchart | Mô hình 3 lớp Client-Application-Data |
| 2 | HÌNH 3.2 | Use Case tổng quát | Use Case | Tất cả actors và use cases của hệ thống |
| 3 | HÌNH 3.3 | ERD tổng quan | ERD | Quan hệ giữa các bảng chính |
| 4 | HÌNH 3.4 | ERD chi tiết Module Tài sản | ERD | Chi tiết 13 bảng module tài sản |
| 5 | HÌNH 3.5 (Part 2) | ERD chi tiết Module Tài chính | ERD | Chi tiết 7 bảng module tài chính |
| 6 | HÌNH 3.5 | Luồng tổng quan hệ thống | Flowchart | 6 giai đoạn vòng đời tài sản |
| 7 | HÌNH 3.6 | Luồng đề xuất mua tài sản | Flowchart | Chi tiết quy trình tạo đề xuất |
| 8 | HÌNH 3.7 | Vòng đời tài sản | State Diagram | Các trạng thái và chuyển đổi |
| 9 | HÌNH 3.8 | Luồng mượn/trả tài sản | Flowchart | 4 bước quy trình mượn trả |
| 10 | HÌNH 3.9 | Luồng kiểm kê tài sản | Flowchart | Chi tiết quy trình kiểm kê |
| 11 | HÌNH 3.10 | Luồng khấu hao tài sản | Flowchart | Khởi tạo, cấu hình, thực hiện khấu hao |
| 12 | HÌNH 3.11 | Luồng thanh lý tài sản | Flowchart | Quy trình bán/tiêu hủy tài sản |
| 13 | HÌNH 3.12 | Dashboard Tổng quan Tài sản | UI Mockup | Giao diện dashboard module tài sản |
| 14 | HÌNH 3.13 | Form Tài sản | UI Mockup | Giao diện form chi tiết tài sản |
| 15 | HÌNH 3.14 | Form Đề xuất mua tài sản | UI Mockup | Giao diện form đề xuất |
| 16 | HÌNH 3.15 | Dashboard Tài chính | UI Mockup | Giao diện dashboard module tài chính |
| 17 | HÌNH 3.16 | Form Phê duyệt mua tài sản | UI Mockup | Giao diện form phê duyệt |
| 18 | HÌNH 3.17 | Mẫu báo cáo tài chính | Report Template | Layout báo cáo tài chính |
| 19 | HÌNH 3.18 | Sơ đồ tích hợp 2 module | Integration Diagram | Các điểm tích hợp chính |
| 20 | HÌNH 3.19 | Sequence Diagram tích hợp | Sequence Diagram | Chi tiết luồng tích hợp mua tài sản |

---

# HƯỚNG DẪN XUẤT HÌNH ẢNH

## Cách 1: Sử dụng Mermaid Live Editor (Khuyến nghị)

1. Truy cập: https://mermaid.live
2. Copy code Mermaid của từng hình vào editor
3. Chỉnh sửa nếu cần
4. Click nút "Export" → Chọn PNG hoặc SVG
5. Đặt tên file theo mã hình (VD: HINH_3_1.png)

## Cách 2: Sử dụng VS Code Extension

1. Cài extension: "Markdown Preview Mermaid Support"
2. Mở file .md này trong VS Code
3. Nhấn Ctrl+Shift+V để preview
4. Chuột phải vào sơ đồ → Save as Image

## Cách 3: Sử dụng Mermaid CLI

```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i input.mmd -o output.png
```

## Lưu ý khi xuất

- Xuất ở độ phân giải cao (scale 2x hoặc 3x) cho chất lượng in ấn
- Sử dụng PNG cho hình có nhiều chi tiết
- Sử dụng SVG nếu cần chỉnh sửa sau
- Đảm bảo font chữ hiển thị đúng tiếng Việt
