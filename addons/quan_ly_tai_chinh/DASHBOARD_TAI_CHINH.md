# 📊 DASHBOARD TỔNG HỢP TÀI CHÍNH - MODULE QLTC

## 📋 Tổng quan

Dashboard Tổng hợp Tài chính là trung tâm quản lý và theo dõi toàn bộ hoạt động tài chính trong module **qltc** (Quản lý Tài chính/Kế toán). Dashboard cung cấp cái nhìn tổng quan, chi tiết và trực quan về:

- 💰 **Đề xuất mua thiết bị**
- 📦 **Tài sản và Khấu hao**
- 📚 **Sổ cái và Bút toán**
- 📈 **Xu hướng và Phân tích**
- 🏢 **Phân bổ theo phòng ban**
- ⚠️ **Cảnh báo và Thông báo**

---

## 🎯 Mục tiêu

1. **Tổng hợp thông tin**: Tập trung tất cả thông tin tài chính quan trọng vào một màn hình duy nhất
2. **Trực quan hóa dữ liệu**: Biểu đồ, sơ đồ giúp dễ dàng phân tích xu hướng
3. **Hỗ trợ quyết định**: Cung cấp số liệu chính xác, kịp thời cho quản lý
4. **Cảnh báo chủ động**: Thông báo các vấn đề cần xử lý ngay
5. **Tiết kiệm thời gian**: Giảm thời gian tìm kiếm, tổng hợp báo cáo

---

## 🏗️ Cấu trúc Dashboard

### 📊 View Kanban (Trang chính)

Dashboard sử dụng **Kanban view** để hiển thị các chỉ số quan trọng dưới dạng thẻ (card) trực quan:

#### 1. Phần Header
- **Tên dashboard**: "Dashboard Tài chính"
- **Ngày hiện tại**: Tự động cập nhật

#### 2. Cảnh báo (Alert Section)
Hiển thị các cảnh báo quan trọng với màu vàng:
- ⚠️ **Tài sản sắp khấu hao hết**: Tài sản còn giá trị < 10%
- ⚠️ **Đề xuất quá hạn**: Đề xuất quá ngày dự kiến nhận

#### 3. Thống kê Đề xuất Mua
- **Tổng đề xuất**: Số lượng tổng (nút bấm lớn màu xanh)
- **Chờ phê duyệt**: Link đến danh sách đề xuất chờ
- **Đã phê duyệt**: Link đến danh sách đã duyệt
- **Tổng giá trị**: Hiển thị số tiền

#### 4. Thống kê Tài sản
- **Tổng tài sản**: Link xem tất cả
- **Tài sản hoạt động**: Link xem tài sản đang hoạt động
- **Giá trị còn lại**: Tổng giá trị hiện tại

#### 5. Thống kê Khấu hao
- **Khấu hao tháng này**: Số tiền khấu hao trong tháng
- **Khấu hao năm này**: Tổng khấu hao từ đầu năm

### 📋 View Form (Chi tiết)

View Form chia thành **5 Tab** chính:

---

### **Tab 1: 📊 Tổng quan**

Hiển thị toàn bộ số liệu thống kê dạng bảng:

#### A. Đề xuất Mua thiết bị
- **Số lượng**:
  - Tổng đề xuất
  - Chờ phê duyệt
  - Đã phê duyệt
  - Bị từ chối
  - Đã mua
  
- **Giá trị**:
  - Tổng giá trị đề xuất
  - Giá trị chờ duyệt
  - Giá trị đã duyệt

#### B. Thống kê Tài sản
- **Số lượng**:
  - Tổng tài sản
  - Tài sản hoạt động
  - Tài sản tạm dừng
  - Tài sản khấu hao hết
  
- **Giá trị**:
  - Tổng giá trị tài sản (ban đầu)
  - Tổng khấu hao tích lũy
  - Tổng giá trị còn lại

#### C. Khấu hao
- Khấu hao tháng này
- Khấu hao quý này
- Khấu hao năm này

#### D. Sổ cái
- Tổng bút toán
- Bút toán tháng này
- Tổng nợ
- Tổng có

---

### **Tab 2: 📈 Xu hướng**

Biểu đồ trực quan hóa xu hướng 12 tháng gần nhất:

#### 1. Biểu đồ Khấu hao (Line Chart)
- **Trục X**: Tháng (MM/YYYY)
- **Trục Y**: Số tiền khấu hao
- **Mục đích**: Theo dõi xu hướng khấu hao tăng/giảm theo thời gian

#### 2. Biểu đồ Mua sắm (Bar Chart)
- **Trục X**: Tháng (MM/YYYY)
- **Trục Y 1**: Giá trị mua sắm
- **Trục Y 2**: Số lượng đề xuất
- **Mục đích**: Phân tích chu kỳ mua sắm, dự đoán nhu cầu

---

### **Tab 3: 🏢 Phòng ban**

Phân tích phân bổ tài sản và chi phí theo từng phòng ban:

#### A. Bảng chi tiết (Tree View)
Các cột:
- **Phòng ban**
- **Số tài sản**: Tổng số tài sản của phòng
- **Giá trị tài sản**: Tổng giá trị còn lại
- **Số đề xuất**: Tổng đề xuất của phòng
- **Giá trị đề xuất**: Tổng chi phí đề xuất

#### B. Biểu đồ cột (Bar Chart)
- So sánh giá trị tài sản và giá trị đề xuất giữa các phòng ban
- Dễ dàng nhận diện phòng nào có nhu cầu cao

#### C. Pivot Table
- Cho phép phân tích linh hoạt
- Tùy chỉnh nhóm, lọc theo nhiều tiêu chí

---

### **Tab 4: 📉 Chi tiết Khấu hao**

Bảng chi tiết khấu hao theo tháng:

| Tháng    | Số tiền khấu hao |
|----------|------------------|
| 01/2025  | 10,000,000 VNĐ   |
| 02/2025  | 12,500,000 VNĐ   |
| ...      | ...              |

**Tổng khấu hao**: Tự động tính ở cuối bảng

---

### **Tab 5: 💰 Chi tiết Mua sắm**

Bảng chi tiết mua sắm theo tháng:

| Tháng    | Số đề xuất | Giá trị mua sắm  |
|----------|------------|------------------|
| 01/2025  | 5          | 50,000,000 VNĐ   |
| 02/2025  | 3          | 30,000,000 VNĐ   |
| ...      | ...        | ...              |

**Tổng**: Tự động tính ở cuối bảng

---

## 🔧 Cấu trúc Kỹ thuật

### Models

#### 1. `dashboard.tai.chinh` (Model chính)
**Chức năng**: Tổng hợp tất cả dữ liệu tài chính

**Fields quan trọng**:
- `name`: Tên dashboard
- `ngay_hien_tai`: Ngày hiện tại (mặc định: hôm nay)
- Thống kê đề xuất: `tong_de_xuat`, `de_xuat_cho_duyet`, `tong_gia_tri_de_xuat`...
- Thống kê tài sản: `tong_tai_san`, `tai_san_hoat_dong`, `tong_gia_tri_tai_san`...
- Thống kê khấu hao: `khau_hao_thang_nay`, `khau_hao_quy_nay`, `khau_hao_nam_nay`...
- Sổ cái: `tong_but_toan`, `tong_no`, `tong_co`...
- Cảnh báo: `canh_bao_tai_san_sap_khau_hao_het`, `canh_bao_de_xuat_qua_han`...

**Computed Fields**: Tất cả field thống kê đều được tính tự động
- `@api.depends('ngay_hien_tai')`: Tự động cập nhật khi ngày thay đổi
- Truy vấn real-time từ các model: `de_xuat_mua_thiet_bi`, `khau_hao`, `account.move`...

**Action Methods**:
- `action_view_de_xuat()`: Mở danh sách đề xuất
- `action_view_de_xuat_cho_duyet()`: Lọc đề xuất chờ duyệt
- `action_view_tai_san()`: Mở danh sách tài sản
- ...

#### 2. `dashboard.depreciation.trend` (Model phụ)
**Chức năng**: Lưu dữ liệu xu hướng khấu hao

**Fields**:
- `dashboard_id`: Liên kết với dashboard
- `month`: Tháng (MM/YYYY)
- `amount`: Số tiền khấu hao

**Computed**: Được tính trong `_compute_trends()` của dashboard

#### 3. `dashboard.purchase.trend` (Model phụ)
**Chức năng**: Lưu dữ liệu xu hướng mua sắm

**Fields**:
- `dashboard_id`: Liên kết với dashboard
- `month`: Tháng (MM/YYYY)
- `amount`: Giá trị mua sắm
- `count`: Số lượng đề xuất

#### 4. `dashboard.department.distribution` (Model phụ)
**Chức năng**: Phân bổ theo phòng ban

**Fields**:
- `dashboard_id`: Liên kết với dashboard
- `department_id`: Phòng ban
- `tai_san_count`: Số tài sản
- `tai_san_value`: Giá trị tài sản
- `de_xuat_count`: Số đề xuất
- `de_xuat_value`: Giá trị đề xuất

---

### Views

#### 1. `view_dashboard_tai_chinh_form`
- Type: Form
- Chức năng: Hiển thị chi tiết dashboard với 5 tab
- Tính năng: `create="false" edit="false" delete="false"` (chỉ đọc)

#### 2. `view_dashboard_tai_chinh_kanban`
- Type: Kanban
- Chức năng: Hiển thị dashboard dạng thẻ
- Tính năng: Click vào các nút để chuyển đến danh sách chi tiết

#### 3. `action_dashboard_tai_chinh`
- Type: `ir.actions.act_window`
- View mode: `kanban,form`
- Mở dashboard với view Kanban mặc định

---

### Data Files

#### `data/dashboard_data.xml`
- Tạo bản ghi dashboard mặc định khi cài đặt module
- `noupdate="1"`: Chỉ tạo 1 lần, không ghi đè khi upgrade

---

### Security

#### `security/ir.model.access.csv`
Quyền truy cập:
- `dashboard.tai.chinh`: Chỉ đọc (`perm_read=1`, các quyền khác = 0)
- `dashboard.depreciation.trend`: Chỉ đọc
- `dashboard.purchase.trend`: Chỉ đọc
- `dashboard.department.distribution`: Chỉ đọc

**Lý do**: Dashboard là báo cáo tổng hợp, không cho phép tạo/sửa/xóa thủ công

---

### Menu Structure

```
📊 Quản lý tài chính/kế toán
 └─ 📊 Dashboard Tài chính (sequence=0) ← MỚI
 └─ 💰 Đề xuất mua thiết bị (sequence=1)
     ├─ Danh sách đề xuất
     └─ Thống kê đề xuất
 └─ 📦 Khấu hao tài sản (sequence=2)
 └─ 📉 Dòng khấu hao (sequence=3)
 └─ 📚 Bút toán khấu hao (sequence=4)
```

---

## 📊 Sơ đồ Luồng Dữ liệu

```
┌─────────────────────────────────────────────────────────────┐
│                    DASHBOARD TÀI CHÍNH                      │
│                   (dashboard.tai.chinh)                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────┴────────────────────┐
         │                                         │
         ▼                                         ▼
┌─────────────────────┐                  ┌─────────────────────┐
│  ĐỀ XUẤT MUA THIẾT BỊ│                  │   TÀI SẢN & KHẤU HAO│
│ (de_xuat_mua_thiet_bi)│                  │     (khau_hao)      │
└─────────────────────┘                  └─────────────────────┘
         │                                         │
         │                                         │
         ├─ Tổng số đề xuất                        ├─ Tổng tài sản
         ├─ Theo trạng thái                        ├─ Theo trạng thái
         ├─ Tổng giá trị                           ├─ Giá trị ban đầu
         ├─ Xu hướng 12 tháng                      ├─ Khấu hao tích lũy
         └─ Phân bổ phòng ban                      ├─ Giá trị còn lại
                                                   ├─ Khấu hao theo kỳ
                                                   └─ Phân bổ phòng ban
                              │
                              ▼
                  ┌─────────────────────┐
                  │   SỔ CÁI & BÚT TOÁN │
                  │   (account.move)    │
                  └─────────────────────┘
                              │
                              ├─ Tổng bút toán
                              ├─ Bút toán theo kỳ
                              ├─ Tổng nợ
                              └─ Tổng có
```

---

## 📈 Biểu đồ Tính toán

### 1. Tính Khấu hao theo Kỳ

```
Khấu hao tháng này = SUM(khau_hao.line.amount)
                     WHERE date >= start_of_month
                     AND date <= end_of_month
                     AND state = 'depreciated'

Khấu hao quý này   = SUM(khau_hao.line.amount)
                     WHERE date >= start_of_quarter
                     AND date <= end_of_quarter
                     AND state = 'depreciated'

Khấu hao năm này   = SUM(khau_hao.line.amount)
                     WHERE date >= start_of_year
                     AND date <= end_of_year
                     AND state = 'depreciated'
```

### 2. Tính Giá trị Tài sản

```
Giá trị còn lại = Giá trị ban đầu - Khấu hao tích lũy

Tổng giá trị còn lại = SUM(khau_hao.gia_tri_con_lai)
                       FOR ALL khau_hao records
```

### 3. Cảnh báo

```
Tài sản sắp khấu hao hết = COUNT(khau_hao)
                           WHERE (gia_tri_con_lai / gia_tri) * 100 < 10
                           AND state = 'active'

Đề xuất quá hạn = COUNT(de_xuat_mua_thiet_bi)
                  WHERE ngay_du_kien_nhan < TODAY
                  AND state IN ('submitted', 'approved')
```

---

## 🎨 Tính năng Tương tác

### 1. Từ Kanban View
- Click vào số "Tổng đề xuất" → Mở danh sách tất cả đề xuất
- Click vào "Chờ duyệt" → Lọc đề xuất chờ phê duyệt
- Click vào "Tổng tài sản" → Mở danh sách tài sản
- Click vào "Hoạt động" → Lọc tài sản đang hoạt động

### 2. Từ Form View
- Tất cả biểu đồ có thể zoom, pan
- Pivot table cho phép group, filter tùy chỉnh
- Có thể xuất báo cáo Excel/PDF từ các tab

### 3. Cảnh báo
- Hiển thị nổi bật khi có vấn đề
- Màu vàng: Cảnh báo (warning)
- Hiển thị số lượng cụ thể

---

## 🚀 Quy trình Sử dụng

### Bước 1: Truy cập Dashboard
```
Menu: Quản lý tài chính/kế toán > 📊 Dashboard Tài chính
```

### Bước 2: Xem Tổng quan (Kanban View)
- Kiểm tra cảnh báo (nếu có)
- Xem các chỉ số chính: đề xuất, tài sản, khấu hao
- Click vào số liệu để xem chi tiết

### Bước 3: Phân tích Chi tiết (Form View)
- Mở tab "Tổng quan" để xem đầy đủ số liệu
- Chuyển sang tab "Xu hướng" để xem biểu đồ 12 tháng
- Tab "Phòng ban" để phân tích theo đơn vị

### Bước 4: Xuất Báo cáo
- Từ các tab, chọn "Print" hoặc "Export"
- Chọn định dạng: PDF, Excel, CSV

---

## ⚙️ Cấu hình và Tùy chỉnh

### 1. Thêm Chỉ số mới
**Ví dụ**: Thêm "Khấu hao tuần này"

**Bước 1**: Thêm field vào model
```python
# File: models/dashboard_tai_chinh.py
khau_hao_tuan_nay = fields.Float(
    string='Khấu hao tuần này',
    compute='_compute_khau_hao_stats'
)
```

**Bước 2**: Cập nhật hàm compute
```python
def _compute_khau_hao_stats(self):
    # ... existing code ...
    
    # Tuần này
    start_week = today - relativedelta(days=today.weekday())
    end_week = start_week + relativedelta(days=6)
    lines_tuan = KhauHaoLine.search([
        ('date', '>=', start_week),
        ('date', '<=', end_week),
        ('state', '=', 'depreciated')
    ])
    record.khau_hao_tuan_nay = sum(lines_tuan.mapped('amount'))
```

**Bước 3**: Thêm vào view
```xml
<!-- File: views/dashboard_tai_chinh.xml -->
<field name="khau_hao_tuan_nay" widget="monetary"/>
```

### 2. Tùy chỉnh Biểu đồ
- Đổi loại biểu đồ: `type="line"` → `type="bar"`, `type="pie"`
- Thêm field: `<field name="new_field" type="measure"/>`
- Group theo field khác: `<field name="category" type="row"/>`

### 3. Thêm Filter/Group
```xml
<search string="Search Dashboard">
    <filter name="this_month" string="Tháng này" 
            domain="[('ngay_hien_tai', '>=', context_today().strftime('%Y-%m-01'))]"/>
    <group string="Group By">
        <filter name="group_month" string="Tháng" context="{'group_by':'ngay_hien_tai:month'}"/>
    </group>
</search>
```

---

## 📝 Ghi chú Kỹ thuật

### 1. Performance
- Các computed field được cache tự động bởi Odoo
- Sử dụng `store=True` cho các field quan trọng
- One2many cho trend được compute on-the-fly (không store)

### 2. Security
- Dashboard chỉ đọc, không cho phép sửa/xóa
- Dữ liệu được lấy theo quyền của user hiện tại
- Tuân thủ record rules của Odoo

### 3. Upgrade
- Khi upgrade module, data không bị ghi đè (`noupdate="1"`)
- Nếu muốn reset dashboard, xóa bản ghi và upgrade lại

---

## 🔮 Tính năng Mở rộng Tương lai

### 1. Dashboard Động
- Cho phép user tùy chỉnh hiển thị
- Drag & drop widgets
- Lưu cấu hình cá nhân

### 2. Thông báo Real-time
- Cảnh báo qua email khi có vấn đề
- Notification trong Odoo
- Tích hợp với calendar

### 3. So sánh Kỳ
- So sánh tháng này với tháng trước
- % tăng/giảm
- Biểu đồ variance

### 4. Dự đoán (AI/ML)
- Dự đoán chi phí khấu hao 6 tháng tới
- Gợi ý thời điểm mua sắm tối ưu
- Phát hiện bất thường

### 5. Export Nâng cao
- Tự động gửi báo cáo định kỳ
- Templates báo cáo có sẵn
- Tích hợp với BI tools (Power BI, Tableau)

---

## 📚 Tài liệu Liên quan

- [README Module QLTC](../README.md)
- [Tính năng Đề xuất Mua thiết bị](../FEATURE_SUMMARY.md)
- [Sơ đồ Đề xuất](../DIAGRAM_DE_XUAT_MUA_THIET_BI.md)
- [Odoo Dashboard Documentation](https://www.odoo.com/documentation/16.0/developer/tutorials/dashboards.html)

---

## ✅ Checklist Triển khai

- [x] Tạo model `dashboard.tai.chinh`
- [x] Tạo model phụ cho biểu đồ
- [x] Implement computed fields
- [x] Tạo action methods
- [x] Tạo view Kanban
- [x] Tạo view Form với 5 tabs
- [x] Tạo menu và action
- [x] Cấu hình security
- [x] Tạo data mẫu
- [x] Cập nhật `__manifest__.py`
- [x] Viết tài liệu

---

## 🎓 Hướng dẫn Test

### Test 1: Hiển thị Dashboard
1. Upgrade module `qltc`
2. Vào menu: Quản lý tài chính/kế toán > Dashboard Tài chính
3. Kiểm tra hiển thị Kanban view
4. Click vào card để mở Form view

### Test 2: Thống kê Đúng
1. Tạo vài đề xuất mua với trạng thái khác nhau
2. Tạo vài tài sản với khấu hao
3. Refresh dashboard
4. So sánh số liệu với thực tế

### Test 3: Biểu đồ
1. Mở Form view
2. Chuyển sang tab "Xu hướng"
3. Kiểm tra biểu đồ Line và Bar hiển thị đúng
4. Hover vào các điểm để xem tooltip

### Test 4: Tương tác
1. Click vào "Tổng đề xuất" ở Kanban view
2. Kiểm tra mở đúng danh sách
3. Click vào "Chờ duyệt"
4. Kiểm tra filter đúng

### Test 5: Cảnh báo
1. Tạo đề xuất quá hạn
2. Tạo tài sản khấu hao gần hết
3. Refresh dashboard
4. Kiểm tra cảnh báo hiển thị

---

## 🐛 Troubleshooting

### Lỗi: Dashboard không hiển thị
**Nguyên nhân**: Chưa có bản ghi dashboard  
**Giải pháp**: 
```python
# Chạy trong Odoo shell
dashboard = env['dashboard.tai.chinh'].create({'name': 'Dashboard Tài chính'})
```

### Lỗi: Biểu đồ trống
**Nguyên nhân**: Không có dữ liệu 12 tháng  
**Giải pháp**: Tạo dữ liệu mẫu hoặc chờ đủ dữ liệu

### Lỗi: Access denied
**Nguyên nhân**: Thiếu quyền  
**Giải pháp**: Kiểm tra file `ir.model.access.csv`

---

**Tác giả**: Module QLTC Team  
**Ngày tạo**: 2026-01-08  
**Phiên bản**: 1.0  
**Odoo Version**: 16.0
