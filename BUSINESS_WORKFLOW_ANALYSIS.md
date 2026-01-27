# SƠ ĐỒ LUỒNG NGHIỆP VỤ CHI TIẾT - MODULE QUẢN LÝ TÀI SẢN & TÀI CHÍNH

## 📋 TỔNG QUAN SYSTEM

Hệ thống bao gồm 2 module tích hợp chặt chẽ:
- **Module Quản lý Tài sản (quan_ly_tai_san)**: Quản lý vòng đời tài sản
- **Module Quản lý Tài chính (quan_ly_tai_chinh)**: Phê duyệt & Ghi nhận tài chính

---

## 🏗️ KIẾN TRÚC HỆ THỐNG

```mermaid
graph TD
    A[Module Quản lý Tài sản] --> B[Module Quản lý Tài chính]
    B --> A
    
    A --> C[Tạo đề xuất mua]
    A --> D[Quản lý tài sản]
    A --> E[Mượn/Trả tài sản]
    A --> F[Kiểm kê tài sản]
    A --> G[Thanh lý tài sản]
    
    B --> H[Phê duyệt mua]
    B --> I[Ghi nhận tài chính]
    B --> J[Khấu hao tài sản]
    B --> K[Báo cáo tài chính]
```

---

# PHẦN I: MODULE QUẢN LÝ TÀI SẢN

## 1. LUỒNG ĐỀ XUẤT MUA TÀI SẢN

### 📊 Sơ đồ luồng:

```mermaid
flowchart TD
    Start([Bắt đầu]) --> Create[Tạo đề xuất mua tài sản]
    Create --> Draft{Trạng thái: DRAFT}
    Draft --> AddDetails[Thêm chi tiết thiết bị]
    AddDetails --> Validate{Validate dữ liệu}
    Validate -->|Lỗi| AddDetails
    Validate -->|OK| Submit[Gửi đề xuất]
    Submit --> Submitted{Trạng thái: SUBMITTED}
    Submitted --> AutoCreate[Tự động tạo đơn phê duyệt ở module TC]
    AutoCreate --> Waiting{Trạng thái: WAITING_APPROVAL}
    Waiting --> FinanceDecision{Quyết định ở module TC}
    FinanceDecision -->|Phê duyệt| Approved[APPROVED]
    FinanceDecision -->|Từ chối| Rejected[REJECTED]
    Approved --> CreateAssets[Tự động tạo tài sản]
    CreateAssets --> End([Kết thúc])
    Rejected --> End
```

### 🔧 Chi tiết nghiệp vụ:

#### Model: `de_xuat_mua_tai_san`

**States:**
- `draft` → `submitted` → `waiting_approval` → `approved/rejected/cancelled`

**Key Methods:**
- `action_submit()`: Gửi đề xuất, tạo đơn phê duyệt ở module tài chính
- `_create_approval_request()`: Tạo record phe_duyet_mua_tai_san
- `_on_approval_complete()`: Callback khi phê duyệt hoàn tất

**Business Rules:**
1. Phải có ít nhất 1 chi tiết thiết bị
2. Mỗi thiết bị phải có danh mục tài sản
3. Tổng giá trị > 0
4. Chỉ tạo đơn phê duyệt khi state = submitted

---

## 2. LUỒNG QUẢN LÝ TÀI SẢN

### 📊 Sơ đồ vòng đời tài sản:

```mermaid
stateDiagram-v2
    [*] --> TaiSanMoi: Tạo từ đề xuất được duyệt
    TaiSanMoi --> ChuaPhanBo: Mặc định
    ChuaPhanBo --> DaPhanBo: Phân bổ cho phòng ban
    DaPhanBo --> DangSuDung: Nhân viên sử dụng
    DangSuDung --> DaPhanBo: Thu hồi
    DangSuDung --> DaThanhLy: Thanh lý
    DaPhanBo --> DaThanhLy: Thanh lý
    ChuaPhanBo --> DaThanhLy: Thanh lý
    DaThanhLy --> [*]
    
    DangSuDung --> BaoDuong: Bảo dưỡng
    BaoDuong --> DangSuDung: Hoàn tất
    DangSuDung --> KhauHao: Khấu hao định kỳ
    KhauHao --> DangSuDung: Tiếp tục
```

### 🔧 Chi tiết nghiệp vụ:

#### Model: `tai_san`

**Key Fields:**
- `trang_thai_thanh_ly`: Computed từ phân bổ và thanh lý
- `gia_tri_hien_tai`: Được cập nhật qua khấu hao
- `pp_khau_hao`: Phương pháp khấu hao (straight-line/degressive/none)

**Key Methods:**
- `action_tinh_khau_hao()`: Tính khấu hao theo phương pháp
- `_compute_trang_thai_thanh_ly()`: Tính trạng thái từ quan hệ

**Business Rules:**
1. Mã tài sản unique
2. Giá trị hiện tại >= 0
3. Khấu hao chỉ áp dụng khi có phương pháp ≠ 'none'
4. Tài sản đã thanh lý không thể chỉnh sửa

---

## 3. LUỒNG PHÂN BỔ TÀI SẢN

### 📊 Sơ đồ luồng:

```mermaid
flowchart TD
    TaiSan[Tài sản khả dụng] --> ChonPhongBan[Chọn phòng ban]
    ChonPhongBan --> ChonNhanVien[Chọn nhân viên sử dụng]
    ChonNhanVien --> TaoPhanBo[Tạo phân bổ tài sản]
    TaoPhanBo --> InUse{Trạng thái: IN-USE}
    InUse --> TraVe[Thu hồi tài sản]
    TraVe --> NotInUse{Trạng thái: NOT-IN-USE}
    NotInUse --> PhanBoMoi[Phân bổ mới]
    PhanBoMoi --> InUse
```

#### Model: `phan_bo_tai_san`

**States:**
- `in-use`: Đang sử dụng
- `not-in-use`: Không sử dụng

**Business Rules:**
1. Một tài sản có thể có nhiều phân bổ theo thời gian
2. Chỉ có một phân bổ active tại một thời điểm
3. Phân bổ ảnh hưởng đến trạng thái tài sản chính

---

## 4. LUỒNG MƯỢN/TRẢ TÀI SẢN

### 📊 Sơ đồ luồng:

```mermaid
flowchart TD
    Start([Nhân viên cần mượn]) --> TaoDoMuon[Tạo đơn mượn]
    TaoDoMuon --> DangCho{Trạng thái: DANG-CHO}
    DangCho --> QuanLyDuyet{Quản lý duyệt}
    QuanLyDuyet -->|Duyệt| TaoPhieuMuon[Tạo phiếu mượn/trả]
    QuanLyDuyet -->|Từ chối| TuChoi[TU-CHOI]
    TaoPhieuMuon --> DangMuon{Trạng thái: DANG-MUON}
    DangMuon --> Check{Kiểm tra hạn}
    Check -->|Trong hạn| DangMuon
    Check -->|Quá hạn| QuaHan[QUA-HAN]
    DangMuon --> TraTaiSan[Trả tài sản]
    TraTaiSan --> DaTra[DA-TRA]
    TuChoi --> End([Kết thúc])
    DaTra --> End
    QuaHan --> End
```

### 🔧 Chi tiết nghiệp vụ:

#### Model: `don_muon_tai_san`
- Đơn yêu cầu mượn từ nhân viên
- States: `dang-cho`, `da-duyet`, `tu-choi`

#### Model: `muon_tra_tai_san`
- Phiếu mượn/trả được tạo từ đơn mượn đã duyệt
- States: `dang-muon`, `da-tra`
- Compute `tinh_trang`: Dựa trên thời gian hiện tại vs thời hạn

**Business Rules:**
1. Thời gian mượn < thời gian trả
2. Không thể trả quá khứ
3. Một đơn mượn → một phiếu mượn/trả
4. Tài sản phải đang available để mượn

---

## 5. LUỒNG KIỂM KÊ TÀI SẢN

### 📊 Sơ đồ luồng:

```mermaid
flowchart TD
    Start([Định kỳ kiểm kê]) --> TaoPhieu[Tạo phiếu kiểm kê]
    TaoPhieu --> ChonPhongBan[Chọn phòng ban]
    ChonPhongBan --> LoadTaiSan[Load tài sản của phòng ban]
    LoadTaiSan --> KiemKe[Kiểm kê từng tài sản]
    KiemKe --> CheckResult{Kết quả kiểm kê}
    CheckResult -->|Tồn tại| OK[Ghi nhận: Tồn tại]
    CheckResult -->|Thiếu| Missing[Ghi nhận: Thiếu]
    CheckResult -->|Hỏng| Damaged[Ghi nhận: Hỏng]
    OK --> UpdateStatus[Cập nhật trạng thái]
    Missing --> UpdateStatus
    Damaged --> UpdateStatus
    UpdateStatus --> MoreAssets{Còn tài sản?}
    MoreAssets -->|Có| KiemKe
    MoreAssets -->|Không| BaoCao[Tạo báo cáo kiểm kê]
    BaoCao --> End([Kết thúc])
```

#### Model: `kiem_ke_tai_san` & `kiem_ke_tai_san_line`

**States kiểm kê:**
- `in-progress`: Đang kiểm kê
- `finished`: Đã kiểm kê

**Kết quả kiểm kê:**
- `ton-tai`: Tài sản tồn tại, tình trạng bình thường
- `thieu`: Không tìm thấy tài sản
- `hong`: Tài sản hỏng hóc

---

## 6. LUỒNG LUÂN CHUYỂN TÀI SẢN

### 📊 Sơ đồ luồng:

```mermaid
flowchart TD
    Start([Cần luân chuyển]) --> TaoPhieu[Tạo phiếu luân chuyển]
    TaoPhieu --> ChonNguon[Chọn bộ phận nguồn]
    ChonNguon --> ChonDich[Chọn bộ phận đích]
    ChonDich --> ChonTaiSan[Chọn tài sản cần chuyển]
    ChonTaiSan --> Validate{Validate}
    Validate -->|Tài sản đang sử dụng| Warning[Cảnh báo]
    Validate -->|OK| LuanChuyen[Thực hiện luân chuyển]
    Warning --> Confirm{Xác nhận?}
    Confirm -->|Có| LuanChuyen
    Confirm -->|Không| ChonTaiSan
    LuanChuyen --> CapNhatPhanBo[Cập nhật phân bổ]
    CapNhatPhanBo --> TaoLichSu[Tạo lịch sử luân chuyển]
    TaoLichSu --> End([Kết thúc])
```

---

## 7. LUỒNG THANH LÝ TÀI SẢN

### 📊 Sơ đồ luồng:

```mermaid
flowchart TD
    Start([Tài sản cần thanh lý]) --> TaoThanhLy[Tạo phiếu thanh lý]
    TaoThanhLy --> ChonHanhDong{Chọn hành động}
    ChonHanhDong -->|Bán| Ban[Bán tài sản]
    ChonHanhDong -->|Tiêu hủy| TieuHuy[Tiêu hủy tài sản]
    Ban --> NhapGiaBan[Nhập giá bán]
    NhapGiaBan --> ValidateGia{Validate giá}
    ValidateGia -->|Giá > 0| XuLy
    ValidateGia -->|Giá <= 0| NhapGiaBan
    TieuHuy --> XuLy[Xử lý thanh lý]
    XuLy --> CapNhatTrangThai[Cập nhật trạng thái tài sản]
    CapNhatTrangThai --> TaoLichSu[Tạo lịch sử thanh lý]
    TaoLichSu --> End([Kết thúc])
```

**Business Rules:**
1. Một tài sản chỉ thanh lý một lần
2. Giá bán > 0 nếu chọn hành động "bán"
3. Tài sản thanh lý không thể chỉnh sửa
4. Thu hồi phân bổ trước khi thanh lý

---

# PHẦN II: MODULE QUẢN LÝ TÀI CHÍNH

## 1. LUỒNG PHÊ DUYỆT MUA TÀI SẢN

### 📊 Sơ đồ luồng:

```mermaid
flowchart TD
    Receive[Nhận đề xuất từ module TS] --> Review[Xem xét đề xuất]
    Review --> ConfigAccount[Cấu hình tài khoản kế toán]
    ConfigAccount --> Decision{Quyết định}
    Decision -->|Phê duyệt| Approve[action_approve]
    Decision -->|Từ chối| Reject[action_reject]
    
    Approve --> CreateAssets[Tạo tài sản]
    CreateAssets --> CreateJournal[Ghi nhận sổ cái]
    CreateJournal --> CreateDepreciation[Tạo lịch khấu hao]
    CreateDepreciation --> UpdateStatus[Cập nhật trạng thái đề xuất]
    UpdateStatus --> Notify[Thông báo người đề xuất]
    
    Reject --> UpdateStatus2[Cập nhật trạng thái từ chối]
    UpdateStatus2 --> Notify2[Thông báo người đề xuất]
    
    Notify --> End([Kết thúc])
    Notify2 --> End
```

### 🔧 Chi tiết nghiệp vụ:

#### Model: `phe_duyet_mua_tai_san`

**Key Methods:**
- `action_approve()`: Phê duyệt → Tạo tài sản + ghi nhận TC + khấu hao
- `action_reject()`: Từ chối → Cập nhật trạng thái đề xuất
- `_create_assets()`: Tạo tài sản trong module TS
- `_create_journal_entry()`: Ghi bút toán kế toán
- `_create_depreciation_schedule()`: Tạo lịch khấu hao

**Business Logic:**
1. **Tạo tài sản**: Mỗi line tạo nhiều tài sản theo số lượng
2. **Ghi sổ cái**: 
   - Nợ: Tài khoản Tài sản cố định
   - Có: Tài khoản Tiền mặt/Ngân hàng
3. **Khấu hao**: Tự động theo phương pháp và thời gian

---

## 2. LUỒNG KHẤU HAO TÀI SẢN

### 📊 Sơ đồ luồng:

```mermaid
flowchart TD
    Start([Tài sản được tạo]) --> CheckMethod{Có khấu hao?}
    CheckMethod -->|Không| NoDepreciation[Không khấu hao]
    CheckMethod -->|Có| CreateSchedule[Tạo lịch khấu hao]
    CreateSchedule --> CalculateRate[Tính toán mức khấu hao]
    CalculateRate --> MethodCheck{Phương pháp}
    MethodCheck -->|Tuyến tính| Straight[Khấu hao đều hàng năm]
    MethodCheck -->|Giảm dần| Degressive[Khấu hao giảm dần]
    Straight --> CreateEntries[Tạo các bút toán hàng năm]
    Degressive --> CreateEntries
    CreateEntries --> Schedule[Lên lịch tự động]
    Schedule --> MonthlyCheck[Kiểm tra hàng tháng]
    MonthlyCheck --> PostEntry[Ghi nhận bút toán khấu hao]
    PostEntry --> UpdateAssetValue[Cập nhật giá trị tài sản]
    UpdateAssetValue --> CheckComplete{Hoàn thành khấu hao?}
    CheckComplete -->|Chưa| MonthlyCheck
    CheckComplete -->|Hoàn thành| Complete[Khấu hao hoàn tất]
    NoDepreciation --> End([Kết thúc])
    Complete --> End
```

### 🔧 Chi tiết nghiệp vụ:

#### Model: `khau_hao_tai_san` & `lich_khau_hao`

**Phương pháp khấu hao:**
1. **Tuyến tính** (`straight-line`): Giá trị / Số năm
2. **Giảm dần** (`degressive`): Giá trị còn lại × Tỷ lệ%
3. **Không khấu hao** (`none`): Không tạo lịch

**Bút toán khấu hao:**
- Nợ: Chi phí khấu hao (642)
- Có: Khấu hao luỹ kế tài sản cố định (214)

---

## 3. LUỒNG GHI NHẬN SỔ CÁI

### 📊 Sơ đồ luồng:

```mermaid
flowchart TD
    Event[Sự kiện kế toán] --> CreateEntry[Tạo bút toán]
    CreateEntry --> DebitCredit[Nhập Nợ/Có]
    DebitCredit --> Validate{Validate}
    Validate -->|Nợ = Có| Post[Ghi sổ]
    Validate -->|Nợ ≠ Có| Error[Lỗi cân đối]
    Error --> DebitCredit
    Post --> UpdateGL[Cập nhật sổ cái]
    UpdateGL --> CreateReport[Tạo báo cáo]
    CreateReport --> End([Kết thúc])
```

#### Model: `but_toan`

**States:**
- `draft`: Nháp
- `posted`: Đã ghi sổ

**Business Rules:**
1. Tổng nợ = Tổng có
2. Chỉ bút toán posted mới ảnh hưởng báo cáo
3. Tự động tạo số chứng từ

---

## 4. LUỒNG BÁO CÁO TÀI CHÍNH

### 📊 Sơ đồ luồng:

```mermaid
flowchart TD
    Request[Yêu cầu báo cáo] --> SelectType{Chọn loại báo cáo}
    SelectType -->|Bảng cân đối| BalanceSheet[Bảng cân đối kế toán]
    SelectType -->|Báo cáo KQ| ProfitLoss[Báo cáo kết quả KD]
    SelectType -->|Dòng tiền| CashFlow[Báo cáo lưu chuyển tiền tệ]
    SelectType -->|Khấu hao| Depreciation[Báo cáo khấu hao]
    
    BalanceSheet --> GatherData1[Thu thập dữ liệu từ sổ cái]
    ProfitLoss --> GatherData2[Thu thập dữ liệu từ sổ cái]
    CashFlow --> GatherData3[Thu thập dữ liệu từ sổ cái]
    Depreciation --> GatherData4[Thu thập dữ liệu khấu hao]
    
    GatherData1 --> Calculate1[Tính toán số liệu]
    GatherData2 --> Calculate2[Tính toán số liệu]
    GatherData3 --> Calculate3[Tính toán số liệu]
    GatherData4 --> Calculate4[Tính toán số liệu]
    
    Calculate1 --> Present1[Trình bày báo cáo]
    Calculate2 --> Present2[Trình bày báo cáo]
    Calculate3 --> Present3[Trình bày báo cáo]
    Calculate4 --> Present4[Trình bày báo cáo]
    
    Present1 --> End([Xuất báo cáo])
    Present2 --> End
    Present3 --> End
    Present4 --> End
```

#### Model: `bao_cao_tai_chinh`

**Loại báo cáo:**
- Bảng cân đối kế toán
- Báo cáo kết quả kinh doanh  
- Báo cáo lưu chuyển tiền tệ
- Báo cáo khấu hao tài sản

---

## 5. DASHBOARD TÀI CHÍNH

### 📊 Sơ đồ KPI:

```mermaid
graph TD
    Dashboard[Dashboard Tài chính] --> A[Phê duyệt mua TS]
    Dashboard --> B[Khấu hao TS]
    Dashboard --> C[Bút toán]
    Dashboard --> D[Tài khoản]
    
    A --> A1[Tổng đơn phê duyệt]
    A --> A2[Chờ phê duyệt] 
    A --> A3[Đã phê duyệt]
    A --> A4[Giá trị phê duyệt]
    
    B --> B1[Tổng tài sản]
    B --> B2[Đang khấu hao]
    B --> B3[Khấu hao tháng này]
    B --> B4[Giá trị còn lại]
    
    C --> C1[Bút toán tháng này]
    C --> C2[Tổng nợ]
    C --> C3[Tổng có]
    
    D --> D1[Tài khoản hoạt động]
    D --> D2[Số dư tài khoản]
```

#### Model: `dashboard.tai.chinh`

**Real-time Metrics:**
- Cập nhật theo `ngay_hien_tai`
- Compute từ các model liên quan
- Action methods để drill-down chi tiết

---

# PHẦN III: TÍCH HỢP 2 MODULE

## 1. LUỒNG TÍCH HỢP CHÍNH

### 📊 Sơ đồ tổng thể:

```mermaid
sequenceDiagram
    participant NV as Nhân viên
    participant TS as Module Tài sản
    participant TC as Module Tài chính
    participant SoCai as Sổ cái
    participant Asset as Tài sản
    
    NV->>TS: 1. Tạo đề xuất mua
    TS->>TS: 2. Validate & Save
    NV->>TS: 3. Gửi đề xuất
    TS->>TC: 4. Tạo đơn phê duyệt
    TC->>TC: 5. Lưu đơn phê duyệt
    
    Note over TC: Quản lý tài chính xem xét
    
    TC->>TC: 6. Phê duyệt
    TC->>Asset: 7. Tạo tài sản
    TC->>SoCai: 8. Ghi sổ cái
    TC->>TC: 9. Tạo lịch khấu hao
    TC->>TS: 10. Cập nhật trạng thái
    TS->>NV: 11. Thông báo kết quả
```

---

## 2. NGHIỆP VỤ PHÁT SINH KHI TÍCH HỢP

### 🔄 Đồng bộ dữ liệu

```mermaid
graph TD
    A[Tạo tài sản ở Module TC] --> B[Đồng bộ sang Module TS]
    B --> C{Validation}
    C -->|OK| D[Cập nhật liên kết]
    C -->|Fail| E[Rollback + Log error]
    D --> F[Notification]
    E --> G[Manual retry]
```

**Key Integration Points:**

1. **Đề xuất → Phê duyệt**
   - Module TS: `de_xuat_mua_tai_san._create_approval_request()`
   - Module TC: `phe_duyet_mua_tai_san.create()`

2. **Phê duyệt → Tài sản**
   - Module TC: `phe_duyet_mua_tai_san.action_approve()`
   - Module TS: `tai_san.create()` (multiple)

3. **Tài sản → Khấu hao**
   - Module TC: `khau_hao_tai_san.create()`
   - Auto schedule: `lich_khau_hao.create()` (multiple)

### 🛠️ Error Handling

```mermaid
flowchart TD
    Process[Quy trình tích hợp] --> Error{Có lỗi?}
    Error -->|Không| Success[Thành công]
    Error -->|Có| Identify[Xác định loại lỗi]
    Identify --> DataError{Data Error?}
    Identify --> SystemError{System Error?}
    
    DataError -->|Validation| Rollback1[Rollback + User notification]
    SystemError -->|Network/DB| Rollback2[Rollback + Log + Retry]
    
    Rollback1 --> ManualFix[Sửa thủ công]
    Rollback2 --> AutoRetry[Retry tự động]
    
    ManualFix --> Process
    AutoRetry --> Process
    Success --> End([Kết thúc])
```

### 📊 Workflow Monitoring

```mermaid
graph TD
    Monitor[Monitoring System] --> Status1[Đề xuất Status]
    Monitor --> Status2[Phê duyệt Status] 
    Monitor --> Status3[Tài sản Status]
    Monitor --> Status4[Khấu hao Status]
    
    Status1 --> Alert1{Alert needed?}
    Status2 --> Alert2{Alert needed?}
    Status3 --> Alert3{Alert needed?}
    Status4 --> Alert4{Alert needed?}
    
    Alert1 -->|Yes| Notify[Send notification]
    Alert2 -->|Yes| Notify
    Alert3 -->|Yes| Notify  
    Alert4 -->|Yes| Notify
    
    Notify --> Log[Log to system]
    Log --> Dashboard[Update dashboard]
```

---

# PHẦN IV: NGHIỆP VỤ BỔ SUNG TÍCH HỢP

## 1. TỰ ĐỘNG HÓA QUY TRÌNH

### 📊 Scheduled Jobs:

```mermaid
gantt
    title Lịch trình tự động hóa
    dateFormat  HH:mm
    axisFormat %H:%M
    
    section Hàng ngày
    Kiểm tra đề xuất quá hạn    :done, check1, 00:00, 00:30
    Cập nhật trạng thái mượn    :done, check2, 01:00, 01:30
    Tính khấu hao hàng ngày     :done, dep1,   02:00, 02:30
    
    section Hàng tháng  
    Ghi nhận khấu hao tháng     :crit, dep2,   00:00, 02:00
    Tạo báo cáo tài chính       :crit, report, 08:00, 10:00
    
    section Hàng quý
    Đối soát tài sản            :active, audit, 09:00, 17:00
    Kiểm kê định kỳ            :audit2, 08:00, 17:00
```

### 🔄 Auto-workflows:

1. **Nhắc nhở phê duyệt**: Tự động tạo activity sau 3 ngày
2. **Cảnh báo mượn quá hạn**: Email tự động cho người mượn
3. **Khấu hao hàng tháng**: Batch job tạo bút toán
4. **Kiểm kê định kỳ**: Tự động tạo phiếu kiểm kê theo chu kỳ

---

## 2. BÁO CÁO TÍCH HỢP

### 📊 Cross-module Reports:

```mermaid
graph TD
    Report[Báo cáo tích hợp] --> R1[ROI Tài sản]
    Report --> R2[Chi phí vận hành]
    Report --> R3[Hiệu quả sử dụng]
    Report --> R4[Dự báo khấu hao]
    
    R1 --> Data1[Giá mua + Giá trị hiện tại + Doanh thu]
    R2 --> Data2[Chi phí mua + Bảo dưỡng + Vận hành]
    R3 --> Data3[Thời gian sử dụng + Tần suất mượn]
    R4 --> Data4[Lịch khấu hao + Trend phân tích]
    
    Data1 --> Chart1[ROI Chart]
    Data2 --> Chart2[Cost Analysis]
    Data3 --> Chart3[Utilization Rate]
    Data4 --> Chart4[Forecasting]
```

---

## 3. BUSINESS INTELLIGENCE

### 📈 KPI Dashboard Tích hợp:

```mermaid
graph TD
    BI[Business Intelligence] --> KPI1[Asset Utilization]
    BI --> KPI2[Financial Performance]
    BI --> KPI3[Process Efficiency]
    BI --> KPI4[Risk Management]
    
    KPI1 --> M1[% Tài sản đang sử dụng]
    KPI1 --> M2[Tần suất mượn/trả]
    KPI1 --> M3[Thời gian idle]
    
    KPI2 --> M4[ROI trung bình]
    KPI2 --> M5[Chi phí khấu hao/tài sản]
    KPI2 --> M6[Chu kỳ hoàn vốn]
    
    KPI3 --> M7[Thời gian phê duyệt TB]
    KPI3 --> M8[% Đề xuất được duyệt]
    KPI3 --> M9[Thời gian từ mua đến sử dụng]
    
    KPI4 --> M10[Tài sản mất mát]
    KPI4 --> M11[Tài sản hỏng hóc]
    KPI4 --> M12[Rủi ro thanh khoản]
```

---

# PHẦN V: SECURITY & COMPLIANCE

## 1. PHÂN QUYỀN NGHIỆP VỤ

```mermaid
graph TD
    Roles[User Roles] --> Admin[System Admin]
    Roles --> AssetManager[Asset Manager] 
    Roles --> FinanceManager[Finance Manager]
    Roles --> Employee[Employee]
    
    Admin --> A1[Full access both modules]
    
    AssetManager --> A2[Create/Edit Assets]
    AssetManager --> A3[Asset Allocation]
    AssetManager --> A4[Create Proposals]
    AssetManager --> A5[Asset Reports]
    
    FinanceManager --> F1[Approve Proposals]
    FinanceManager --> F2[Financial Records]
    FinanceManager --> F3[Depreciation Setup]
    FinanceManager --> F4[Financial Reports]
    
    Employee --> E1[Create Borrow Requests]
    Employee --> E2[View Own Requests]
    Employee --> E3[Basic Asset Info]
```

## 2. AUDIT TRAIL

```mermaid
sequenceDiagram
    participant User
    participant System
    participant AuditLog
    participant Database
    
    User->>System: Thực hiện action
    System->>AuditLog: Log action details
    AuditLog->>Database: Store log
    System->>Database: Update data
    System->>User: Return result
    
    Note over AuditLog: User, Time, Action, Before/After values
```

**Tracking Points:**
- Tất cả thay đổi trạng thái đề xuất/phê duyệt
- Phân bổ/thu hồi tài sản
- Ghi nhận tài chính
- Thay đổi giá trị tài sản

---

# PHẦN VI: PERFORMANCE & SCALABILITY

## 1. OPTIMIZATION STRATEGIES

### 📊 Database Optimization:

```mermaid
graph TD
    DB[Database Optimization] --> Index1[Index on frequently queried fields]
    DB --> Archive[Archive old records]
    DB --> Partition[Partition large tables]
    
    Index1 --> I1[tai_san.ma_tai_san]
    Index1 --> I2[phe_duyet_mua_tai_san.state]
    Index1 --> I3[khau_hao_tai_san.ngay_bat_dau]
    
    Archive --> A1[Archived proposals > 2 years]
    Archive --> A2[Completed depreciation schedules]
    
    Partition --> P1[Partition by year]
    Partition --> P2[Partition by department]
```

### 🔄 Caching Strategy:

```mermaid
graph TD
    Cache[Caching Layer] --> Redis1[Dashboard metrics]
    Cache --> Redis2[User permissions]
    Cache --> Redis3[Department assets]
    
    Redis1 --> Refresh1[Refresh every hour]
    Redis2 --> Refresh2[Refresh on role change]
    Redis3 --> Refresh3[Refresh on asset change]
```

---

# KẾT LUẬN

## ✅ ĐIỂM MẠNH HỆ THỐNG

1. **Tách biệt trách nhiệm rõ ràng**: Tài sản vs Tài chính
2. **Workflow tự động hóa**: Giảm thiểu can thiệp thủ công
3. **Tính toàn vẹn dữ liệu**: Validation và rollback cơ chế
4. **Truy vết đầy đủ**: Audit trail cho mọi thay đổi
5. **Báo cáo đa chiều**: Kết hợp cả 2 module

## 🎯 KHUYẾN NGHỊ PHÁT TRIỂN

1. **Mobile App**: Cho việc kiểm kê và mượn/trả
2. **AI/ML**: Dự báo nhu cầu mua sắm và khấu hao
3. **IoT Integration**: Tracking vị trí tài sản real-time
4. **API Gateway**: Tích hợp với hệ thống ERP khác
5. **Blockchain**: Đảm bảo tính bất biến của lịch sử tài sản

---

*Tài liệu này cung cấp cái nhìn tổng quan về luồng nghiệp vụ của hệ thống quản lý tài sản và tài chính. Mỗi luồng có thể được mở rộng với chi tiết kỹ thuật và business rules cụ thể hơn.*