# DANH SÁCH CHỨC NĂNG CHI TIẾT - HỆ THỐNG QUẢN LÝ TÀI SẢN & TÀI CHÍNH

## 📋 TỔNG QUAN HỆ THỐNG

**Hệ thống bao gồm 2 module tích hợp:**
1. **Module Quản lý Tài sản** (`quan_ly_tai_san`)
2. **Module Quản lý Tài chính** (`quan_ly_tai_chinh`)

---

# PHẦN I: MODULE QUẢN LÝ TÀI SẢN

## 🏠 1. DASHBOARD - TỔNG QUAN TÀI SẢN

### 📊 Dashboard Tổng quan
**Menu**: Dashboard → Tổng quan  
**Model**: `asset.dashboard`  
**Chức năng**:
- **Thống kê tài sản tổng quan**:
  - Tổng số tài sản trong hệ thống
  - Số tài sản đang sử dụng
  - Số tài sản không sử dụng
  - Số tài sản đã thanh lý
- **Thống kê giá trị**:
  - Tổng giá trị ban đầu
  - Tổng giá trị hiện tại
  - Tổng giá trị đã khấu hao
- **Biểu đồ phân bổ theo**:
  - Loại tài sản (Pie chart)
  - Phòng ban (Bar chart)
  - Trạng thái sử dụng (Doughnut chart)

### 📊 Dashboard Mượn trả
**Menu**: Dashboard → Danh sách mượn trả  
**Model**: `asset.dashboard`  
**Chức năng**:
- **Thống kê đơn mượn**:
  - Số đơn mượn chờ duyệt
  - Số đơn đã duyệt chưa trả
  - Số tài sản đang được mượn
- **Top tài sản được mượn nhiều nhất**
- **Cảnh báo đơn mượn quá hạn**
- **Lịch sử mượn trả gần đây**

---

## 🏗️ 2. QUẢN LÝ TÀI SẢN CƠ BẢN

### 📝 2.1. Danh mục tài sản
**Menu**: Tài sản → Loại tài sản  
**Model**: `danh_muc_tai_san`  
**Chức năng**:
- **Tạo/Sửa/Xóa danh mục tài sản**:
  - Mã loại tài sản (unique)
  - Tên loại tài sản
  - Mô tả loại tài sản
- **Tự động tính số lượng tài sản** của mỗi loại
- **Hiển thị danh sách tài sản** thuộc loại

### 🏷️ 2.2. Quản lý tài sản cụ thể
**Menu**: Tài sản → Quản lý tài sản cụ thể  
**Model**: `tai_san`  
**Chức năng**:
- **Thông tin cơ bản**:
  - Mã tài sản (unique, tự động tạo)
  - Tên tài sản
  - Ngày mua tài sản
  - Đơn vị tiền tệ (VNĐ/USD)
  - Giá trị ban đầu/hiện tại
  - Danh mục tài sản
- **Quản lý file đính kèm**:
  - Giấy tờ liên quan (PDF, Word...)
  - Hình ảnh tài sản (JPG, PNG...)
- **Khấu hao tài sản**:
  - Phương pháp: Tuyến tính/Giảm dần/Không khấu hao
  - Thời gian sử dụng tối đa
  - Tỷ lệ khấu hao (%)
  - **Tính khấu hao tự động** (`action_tinh_khau_hao`)
- **Theo dõi trạng thái**:
  - Chưa phân bổ/Đã phân bổ/Đã thanh lý
  - Tự động cập nhật từ phân bổ và thanh lý
- **Lịch sử liên quan**:
  - Lịch sử khấu hao
  - Lịch sử kiểm kê
  - Phiếu luân chuyển
  - Lịch sử thanh lý

### 📍 2.3. Phân bổ tài sản
**Menu**: Tài sản → Phân bổ tài sản  
**Model**: `phan_bo_tai_san`  
**Chức năng**:
- **Phân bổ cho phòng ban**:
  - Chọn tài sản cần phân bổ
  - Chọn phòng ban nhận tài sản
  - Chọn nhân viên sử dụng cụ thể
  - Ngày phân bổ
- **Quản lý trạng thái sử dụng**:
  - Đang sử dụng/Không sử dụng
  - Tình trạng vật lý: Bình thường/Đang mượn/Hư hỏng/Mất
- **Theo dõi vị trí tài sản**
- **Ghi chú và lịch sử phân bổ**

---

## 🔄 3. QUY TRÌNH MUA TÀI SẢN

### 📋 3.1. Đề xuất mua tài sản  
**Menu**: Đề xuất mua tài sản  
**Model**: `de_xuat_mua_tai_san` & `de_xuat_mua_tai_san.line`  
**Chức năng**:

#### Tạo đề xuất
- **Thông tin cơ bản**:
  - Mã đề xuất (auto-generate)
  - Tiêu đề đề xuất
  - Ngày đề xuất
  - Người đề xuất (auto-fill current user)
  - Phòng ban đề xuất
  - Ngày dự kiến nhận hàng

#### Chi tiết thiết bị
- **Thêm/xóa/sửa dòng thiết bị**:
  - Tên thiết bị
  - Danh mục tài sản
  - Mô tả chi tiết
  - Thông số kỹ thuật
  - Số lượng & đơn vị tính
  - Đơn giá & thành tiền
  - Phương pháp khấu hao dự kiến
  - Thời gian sử dụng dự kiến
  - Nhà cung cấp đề xuất

#### Workflow quản lý
- **Trạng thái**: Draft → Submitted → Waiting_Approval → Approved/Rejected/Cancelled
- **Actions**:
  - `action_submit()`: Gửi đề xuất và tạo đơn phê duyệt ở module tài chính
  - `action_reset_to_draft()`: Đưa về trạng thái nháp
  - `action_cancel()`: Hủy đề xuất

#### Tính năng bổ sung
- **File đính kèm**: Báo giá, hình ảnh, tài liệu kỹ thuật
- **Lý do & mô tả**: HTML rich text
- **Tự động tính tổng giá trị**
- **Liên kết với đơn phê duyệt** ở module tài chính
- **Theo dõi tài sản được tạo** sau phê duyệt

---

## 🎯 4. QUẢN LÝ MƯỢN TRẢ TÀI SẢN

### 📝 4.1. Đơn mượn tài sản
**Menu**: Mượn trả tài sản → Đơn mượn tài sản  
**Model**: `don_muon_tai_san` & `don_muon_tai_san_line`  
**Chức năng**:
- **Tạo đơn mượn**:
  - Mã đơn mượn (auto-generate)
  - Tên đơn mượn
  - Phòng ban cho mượn
  - Thời gian mượn/trả dự kiến
  - Nhân viên mượn
  - Lý do mượn
- **Chi tiết tài sản mượn**:
  - Chọn tài sản từ phòng ban
  - Ghi chú cho từng tài sản
- **Workflow phê duyệt**:
  - Trạng thái: Đang chờ → Đã duyệt → Từ chối
  - `action_duyet_don()`: Duyệt đơn mượn
  - `action_tu_choi_don()`: Từ chối với lý do

### 📋 4.2. Quản lý mượn trả tài sản
**Menu**: Mượn trả tài sản → Quản lý mượn trả tài sản  
**Model**: `muon_tra_tai_san` & `muon_tra_tai_san_line`  
**Chức năng**:
- **Tạo phiếu mượn/trả** từ đơn mượn đã duyệt
- **Theo dõi trạng thái**:
  - Đang mượn/Đã trả
  - Tính trạng: Đang mượn/Quá hạn/Chưa tới hạn
- **Quản lý danh sách tài sản**:
  - Tài sản đã mượn
  - Tài sản chưa mượn (computed)
- **Workflow trả tài sản**:
  - `action_tra_tai_san()`: Trả tài sản
  - Cập nhật trạng thái tự động

---

## 🔍 5. KIỂM KÊ TÀI SẢN

### 📊 5.1. Kiểm kê tài sản
**Menu**: Khấu hao/Kiểm kê → Kiểm kê tài sản  
**Model**: `kiem_ke_tai_san` & `kiem_ke_tai_san_line`  
**Chức năng**:
- **Tạo phiếu kiểm kê**:
  - Mã phiếu kiểm kê (auto-generate)
  - Tên phiếu kiểm kê
  - Phòng ban cần kiểm kê
  - Nhân viên thực hiện kiểm kê
  - Thời gian tạo phiếu
- **Load tài sản theo phòng ban**:
  - Tự động load tất cả tài sản của phòng ban
  - Hiển thị danh sách tài sản chưa kiểm kê
- **Thực hiện kiểm kê**:
  - Kết quả: Tồn tại/Thiếu/Hỏng
  - Ghi chú tình trạng
  - Ảnh chụp hiện trạng
- **Trạng thái phiếu**:
  - Chưa kiểm kê/Đã kiểm kê (computed từ chi tiết)

---

## 📈 6. KHẤU HAO TÀI SẢN

### 📊 6.1. Khấu hao tài sản  
**Menu**: Khấu hao/Kiểm kê → Khấu hao tài sản  
**Model**: `lich_su_khau_hao`  
**Chức năng**:
- **Xem lịch sử khấu hao** tất cả tài sản
- **Theo dõi chi tiết**:
  - Mã tài sản & tên tài sản
  - Giá trị ban đầu/hiện tại
  - Phương pháp khấu hao
  - Số tiền khấu hao định kỳ
  - Ngày khấu hao
- **Tính khấu hao theo phương pháp**:
  - **Tuyến tính**: Giá trị / Số năm sử dụng
  - **Giảm dần**: Giá trị còn lại × Tỷ lệ%
- **Ghi chú và theo dõi**

---

## 🔄 7. LUÂN CHUYỂN TÀI SẢN

### 📋 7.1. Quản lý luân chuyển tài sản
**Menu**: Luân chuyển/Thanh lý → Quản lý luân chuyển tài sản  
**Model**: `luan_chuyen_tai_san` & `luan_chuyen_tai_san_line`  
**Chức năng**:
- **Tạo phiếu luân chuyển**:
  - Mã phiếu luân chuyển (auto-generate)
  - Bộ phận nguồn (phòng ban hiện tại)
  - Bộ phận đích (phòng ban chuyển tới)
  - Thời gian luân chuyển
  - Lý do luân chuyển
- **Chi tiết tài sản chuyển**:
  - Chọn tài sản từ bộ phận nguồn
  - Tình trạng tài sản
  - Ghi chú
- **Xử lý tự động**:
  - Cập nhật phân bổ tài sản
  - Tạo lịch sử luân chuyển
  - Thông báo bộ phận liên quan

---

## 🗑️ 8. THANH LÝ TÀI SẢN

### 📋 8.1. Thanh lý tài sản
**Menu**: Luân chuyển/Thanh lý → Thanh lý tài sản  
**Model**: `thanh_ly_tai_san`  
**Chức năng**:
- **Hành động thanh lý**:
  - **Bán**: Nhập giá bán (>0)
  - **Tiêu hủy**: Không có giá bán
- **Thông tin thanh lý**:
  - Mã thanh lý (auto-generate)
  - Tài sản thanh lý
  - Người thực hiện
  - Thời gian thanh lý
  - Lý do thanh lý
- **Tính toán tài chính**:
  - Giá gốc (computed từ tài sản)
  - Lãi/lỗ khi thanh lý
- **Business rules**:
  - Một tài sản chỉ thanh lý một lần
  - Tự động cập nhật trạng thái tài sản
  - Thu hồi phân bổ trước khi thanh lý

---

## 📊 9. LỊCH SỬ VÀ THEO DÕI

### 📈 9.1. Lịch sử kỹ thuật
**Menu**: (Integrated in asset form)  
**Model**: `lich_su_ky_thuat`  
**Chức năng**:
- **Ghi nhận tình trạng kỹ thuật** tài sản theo thời gian
- **Theo dõi bảo dưỡng, sửa chữa**
- **Lịch sử thay đổi cấu hình**

---

# PHẦN II: MODULE QUẢN LÝ TÀI CHÍNH

## 🏠 1. DASHBOARD TÀI CHÍNH

### 📊 1.1. Dashboard tổng hợp
**Menu**: Dashboard  
**Model**: `dashboard.tai.chinh`  
**Chức năng**:

#### Thống kê phê duyệt mua tài sản
- **Tổng quan đơn phê duyệt**:
  - Tổng số đơn phê duyệt
  - Đơn chờ phê duyệt
  - Đơn đã phê duyệt  
  - Đơn hoàn thành
  - Đơn bị từ chối
- **Thống kê giá trị**:
  - Tổng giá trị phê duyệt
  - Giá trị chờ duyệt
  - Giá trị đã duyệt

#### Thống kê khấu hao & tài sản
- **Thống kê tài sản**:
  - Tổng số tài sản
  - Tài sản hoạt động
  - Tài sản đang khấu hao
  - Tài sản hoàn thành khấu hao
- **Thống kê giá trị**:
  - Tổng giá trị tài sản
  - Tổng khấu hao tích lũy
  - Tổng giá trị còn lại
- **Khấu hao theo thời gian**:
  - Khấu hao tháng này
  - Khấu hao quý này
  - Khấu hao năm này

#### Thống kê sổ cái
- **Bút toán kế toán**:
  - Tổng bút toán
  - Bút toán nháp
  - Bút toán đã ghi sổ
  - Tổng giá trị bút toán

#### Thống kê kế toán quản trị
- **Tài khoản quản trị**:
  - Tổng tài khoản
  - Tổng doanh thu
  - Tổng chi phí
  - Chi phí tháng này

#### Actions & Drill-down
- **Action methods**: Từ dashboard nhảy vào chi tiết
  - `action_view_phe_duyet()`: Xem danh sách phê duyệt
  - `action_view_khau_hao()`: Xem lịch khấu hao
  - `action_view_tai_san()`: Xem danh sách tài sản
  - `action_view_but_toan()`: Xem bút toán
  - `action_view_tai_khoan()`: Xem tài khoản

#### Biểu đồ & trực quan hóa
- **Data cho OWL Components**:
  - `get_dashboard_data()`: Metrics tổng quan
  - `get_chart_data()`: Dữ liệu biểu đồ
- **Trend analysis**: Xu hướng theo thời gian
- **Department distribution**: Phân bổ theo phòng ban

---

## ✅ 2. PHÊ DUYỆT MUA TÀI SẢN

### 📋 2.1. Phê duyệt mua tài sản
**Menu**: Phê duyệt mua tài sản  
**Model**: `phe_duyet_mua_tai_san` & `phe_duyet_mua_tai_san.line`  
**Chức năng**:

#### Nhận đề xuất từ module tài sản
- **Liên kết đề xuất gốc**:
  - Mã đề xuất (computed từ đề xuất gốc)
  - Thông tin người đề xuất
  - Phòng ban đề xuất
  - Ngày đề xuất
- **Chi tiết thiết bị** (readonly từ đề xuất):
  - Tên thiết bị & danh mục
  - Số lượng, đơn giá, thành tiền
  - Mô tả & thông số kỹ thuật
  - Phương pháp khấu hao dự kiến

#### Cấu hình tài chính
- **Thiết lập tài khoản kế toán**:
  - Tài khoản tài sản cố định (VD: 211)
  - Tài khoản nguồn vốn (VD: 112 - Tiền mặt, 1121 - Ngân hàng)
  - Sổ nhật ký ghi bút toán
- **Cấu hình khấu hao**:
  - Tài khoản chi phí khấu hao (VD: 642)
  - Tài khoản khấu hao lũy kế (VD: 214)

#### Workflow phê duyệt
- **States**: Draft → Approved/Rejected → Done/Cancelled
- **Action phê duyệt** (`action_approve()`):
  1. **Tạo tài sản** trong module tài sản
  2. **Ghi bút toán kế toán**:
     - Nợ: Tài khoản TSCĐ
     - Có: Tài khoản tiền mặt/ngân hàng
  3. **Tạo lịch khấu hao tự động**
  4. **Cập nhật trạng thái đề xuất gốc**
- **Action từ chối** (`action_reject()`):
  - Ghi lý do từ chối
  - Cập nhật trạng thái đề xuất gốc
  - Thông báo người đề xuất

#### Error handling & rollback
- **Xử lý lỗi thông minh**:
  - Nếu tạo tài sản thành công nhưng ghi sổ lỗi → Chỉ log warning
  - Nếu tạo tài sản lỗi → Rollback toàn bộ
  - Cơ chế retry tự động

#### Theo dõi kết quả
- **Danh sách tài sản đã tạo**:
  - Liên kết Many2many tới tài sản
  - Đếm số lượng tài sản được tạo
  - Action `action_view_assets()`: Xem tài sản
- **Journal entries**:
  - Liên kết tới bút toán đã tạo
  - Action `action_view_journal_entry()`: Xem bút toán
- **Lịch khấu hao**:
  - Danh sách khấu hao tự động
  - Theo dõi tiến trình khấu hao

---

## 📊 3. KHẤU HAO TÀI SẢN

### 📈 3.1. Khấu hao tài sản
**Menu**: Khấu hao → Khấu hao tài sản  
**Model**: `khau_hao_tai_san`  
**Chức năng**:
- **Thiết lập khấu hao**:
  - Liên kết với tài sản
  - Liên kết với đơn phê duyệt (nếu từ phê duyệt)
  - Ngày bắt đầu khấu hao
  - Phương pháp khấu hao
  - Số năm khấu hao
- **Tính toán tự động**:
  - Giá trị khấu hao hàng năm
  - Tổng giá trị khấu hao
  - Giá trị còn lại
- **Quản lý trạng thái**:
  - Đang khấu hao/Tạm dừng/Hoàn thành
  - `action_tam_dung()`: Tạm dừng khấu hao
  - `action_tiep_tuc()`: Tiếp tục khấu hao

### 📅 3.2. Lịch khấu hao chi tiết
**Model**: `lich_khau_hao`  
**Chức năng**:
- **Tự động tạo lịch** khi setup khấu hao
- **Chi tiết hàng năm**:
  - Năm khấu hao
  - Ngày khấu hao
  - Giá trị khấu hao
  - Trạng thái đã ghi nhận

### ⚡ 3.3. Tính khấu hao tự động
**Menu**: Khấu hao → Tính khấu hao tự động  
**Model**: `tinh_toan_khau_hao`  
**Chức năng**:
- **Wizard tính khấu hao hàng loạt**
- **Chọn khoảng thời gian** cần tính
- **Tính khấu hao cho tất cả tài sản** có đủ điều kiện
- **Tạo bút toán khấu hao tự động**

---

## 💰 4. KẾ TOÁN VÀ SỔ CÁI

### 📝 4.1. Bút toán
**Menu**: Kế toán → Bút toán  
**Model**: `but_toan`  
**Chức năng**:
- **Tạo bút toán thủ công**:
  - Số bút toán (auto-generate)
  - Ngày ghi sổ
  - Diễn giải
  - Số chứng từ gốc
- **Chi tiết bút toán**:
  - Tài khoản nợ/có
  - Số tiền
  - Diễn giải chi tiết
- **Workflow**:
  - Draft → Posted
  - `action_post()`: Ghi sổ chính thức
  - `action_draft()`: Đưa về nháp
- **Validation**:
  - Tổng nợ = Tổng có
  - Kiểm tra tài khoản hợp lệ

### 🏦 4.2. Tài khoản quản trị
**Menu**: Kế toán → Tài khoản quản trị  
**Model**: `tai_khoan_quan_tri`  
**Chức năng**:
- **Quản lý plan of accounts**:
  - Mã tài khoản
  - Tên tài khoản
  - Phòng ban quản lý
- **Liên kết giao dịch**:
  - Liên kết với đơn phê duyệt mua
  - Ngày ghi nhận
  - Loại giao dịch
  - Số dư tài khoản
- **Báo cáo tài khoản**:
  - Sổ cái chi tiết
  - Số dư cuối kỳ

---

## 📊 5. BÁO CÁO TÀI CHÍNH

### 📈 5.1. Báo cáo tài chính
**Menu**: Báo cáo tài chính  
**Model**: `bao_cao_tai_chinh`  
**Chức năng**:

#### Các loại báo cáo
- **Bảng cân đối kế toán**:
  - Tài sản & Nguồn vốn
  - Phân chia theo nhóm tài khoản
- **Báo cáo kết quả kinh doanh**:
  - Doanh thu
  - Chi phí (bao gồm khấu hao)
  - Lợi nhuận
- **Báo cáo lưu chuyển tiền tệ**:
  - Dòng tiền hoạt động
  - Dòng tiền đầu tư
  - Dòng tiền tài chính
- **Báo cáo khấu hao tài sản**:
  - Chi tiết khấu hao theo tài sản
  - Tổng hợp theo phòng ban
  - Trend khấu hao theo thời gian

#### Tính năng báo cáo
- **Chọn kỳ báo cáo**: Tháng/Quý/Năm
- **Trạng thái**: Nháp/Đang xử lý/Hoàn thành
- **Export**: PDF, Excel
- **Template động**: Customizable layout

#### KPI Dashboard trong báo cáo
- **Doanh thu vs Chi phí**
- **ROI tài sản**
- **Tỷ lệ khấu hao/tài sản**
- **So sánh kỳ trước**

### 📄 5.2. Report templates
**File**: `report/bao_cao_tai_chinh_report.xml`  
**Chức năng**:
- **Template PDF động**
- **Hiển thị KPI boxes**:
  - Doanh thu (màu xanh lá)
  - Tổng chi phí (màu đỏ)  
  - Lợi nhuận (màu xanh dương/vàng)
- **Styling responsive**
- **Multi-currency support**

---

## 🧙‍♂️ 6. WIZARD VÀ UTILITY

### 📋 6.1. Wizard sao chép
**Menu**: (Context menu từ các form)  
**Model**: `wizard_sao_chep`  
**Chức năng**:
- **Sao chép bản ghi** với tùy chọn
- **Chọn fields cần sao chép**
- **Batch operations**
- **Template sao chép** cho các case thường dùng

---

# PHẦN III: CHỨC NĂNG TÍCH HỢP 2 MODULE

## 🔗 1. TÍCH HỢP QUY TRÌNH MUA TÀI SẢN

### 🔄 1.1. Liên kết đề xuất - phê duyệt
**Mô tả**: Kết nối seamless giữa đề xuất (module TS) và phê duyệt (module TC)

**Chức năng**:
- **Tự động tạo đơn phê duyệt**:
  - Khi gửi đề xuất (`action_submit`) → Tự động tạo record `phe_duyet_mua_tai_san`
  - Copy toàn bộ thông tin và chi tiết thiết bị
  - Tạo activity reminder cho finance manager
- **Đồng bộ trạng thái**:
  - Phê duyệt/Từ chối → Cập nhật trạng thái đề xuất gốc
  - Real-time notification cho người đề xuất
- **Liên kết bidirectional**:
  - Từ đề xuất → Xem đơn phê duyệt (`action_view_phe_duyet`)
  - Từ phê duyệt → Xem đề xuất gốc

### 🏗️ 1.2. Tự động tạo tài sản
**Mô tả**: Sau phê duyệt, tự động tạo tài sản trong module TS

**Chức năng**:
- **Bulk asset creation**:
  - Mỗi line thiết bị → Tạo N tài sản theo số lượng
  - Tự động generate mã tài sản unique
  - Copy thông tin từ đề xuất: Tên, danh mục, phương pháp khấu hao...
- **Error handling thông minh**:
  - Validate danh mục tài sản tồn tại
  - Rollback mechanism nếu lỗi
  - Partial success handling
- **Tracking & audit**:
  - Lưu liên kết tài sản được tạo
  - Activity log đầy đủ
  - Đồng bộ ngược về đề xuất gốc

### 💰 1.3. Tự động ghi nhận tài chính  
**Mô tả**: Ghi bút toán kế toán khi phê duyệt mua tài sản

**Chức năng**:
- **Journal entry tự động**:
  - Nợ: 211 - Tài sản cố định hữu hình
  - Có: 112/1121 - Tiền mặt/Ngân hàng (theo cấu hình)
  - Số tiền = Tổng giá trị phê duyệt
- **Flexible configuration**:
  - Admin cấu hình tài khoản default
  - Override cho từng đơn phê duyệt
  - Multi-currency support
- **Integration với accounting module**:
  - Tạo `account.move` entry thực tế (nếu có)
  - Fallback tạo `but_toan` internal

### 📈 1.4. Tự động tạo lịch khấu hao
**Mô tả**: Setup khấu hao cho tài sản mới tạo

**Chức năng**:
- **Khấu hao schedule tự động**:
  - Tạo `khau_hao_tai_san` cho mỗi tài sản
  - Generate `lich_khau_hao` hàng năm
  - Tính toán dựa trên phương pháp đã chọn
- **Smart scheduling**:
  - Start date từ ngày phê duyệt hoặc ngày dự kiến nhận
  - Adjust cho fiscal year
  - Handle pro-rata cho tài sản mua giữa năm

---

## 📊 2. DASHBOARD TÍCH HỢP

### 📈 2.1. Cross-module metrics
**Mô tả**: Dashboard kết hợp metrics từ cả 2 module

**Chức năng**:
- **Asset utilization rate**:
  - % Tài sản đang sử dụng
  - Frequency mượn trả
  - Idle time analysis
- **Financial performance**:
  - ROI trung bình của tài sản
  - Cost per asset category
  - Depreciation impact on P&L
- **Process efficiency**:
  - Average approval time
  - % Proposal approval rate
  - Time từ purchase đến deployment

### 🎯 2.2. Integrated KPI dashboard
**Chức năng**:
- **Real-time sync**: Dashboard cập nhật real-time từ cả 2 module
- **Drill-down capability**: Click KPI → Chi tiết từ module tương ứng
- **Comparative analysis**: So sánh performance theo department/time
- **Alerting system**: Cảnh báo khi có vấn đề cần attention

---

## 📋 3. BÁO CÁO TÍCH HỢP

### 📊 3.1. Asset lifecycle report
**Mô tả**: Báo cáo toàn bộ vòng đời tài sản

**Chức năng**:
- **From proposal to disposal**:
  - Proposal date → Approval → Asset creation → Deployment → Retirement
  - Cost analysis tại mỗi giai đoạn
  - ROI calculation
- **Department performance**:
  - Asset request vs approval rate
  - Usage efficiency by department
  - Cost center analysis

### 📈 3.2. Financial impact report
**Mô tả**: Impact của tài sản lên tài chính doanh nghiệp

**Chức năng**:
- **Balance sheet impact**:
  - Fixed assets value trend
  - Accumulated depreciation
  - Net book value evolution
- **P&L impact**:
  - Depreciation expense by period
  - Asset disposal gain/loss
  - Maintenance cost allocation
- **Cash flow impact**:
  - Capital expenditure planning
  - Asset financing analysis

### 📊 3.3. Compliance & audit report
**Chức năng**:
- **Approval audit trail**: Toàn bộ quy trình phê duyệt
- **Asset movement tracking**: Di chuyển, mượn trả, thanh lý
- **Financial reconciliation**: Đối soát giữa asset register và general ledger
- **Variance analysis**: Phân tích chênh lệch estimated vs actual cost

---

## 🤖 4. TỰ ĐỘNG HÓA QUY TRÌNH

### ⏰ 4.1. Scheduled jobs
**Mô tả**: Các job tự động chạy background

**Chức năng**:
- **Daily jobs**:
  - Check overdue proposals (>3 days) → Send reminder
  - Update asset borrowing status
  - Calculate daily depreciation
- **Monthly jobs**:
  - Batch depreciation posting
  - Generate monthly financial reports
  - Asset valuation update
- **Quarterly jobs**:
  - Asset audit scheduling
  - Performance metrics compilation

### 📧 4.2. Notification system
**Chức năng**:
- **Proposal workflow**:
  - New proposal → Notify finance team
  - Approval/Rejection → Notify requester
  - Asset created → Notify asset manager
- **Asset management**:
  - Overdue borrowing → Notify borrower & manager
  - Asset due for maintenance → Notify responsible person
  - Depreciation completion → Notify finance
- **Escalation rules**:
  - Overdue approval → Escalate to senior manager
  - Missing assets in audit → Alert security

### 🔄 4.3. Data synchronization
**Chức năng**:
- **Real-time sync**: Changes trong một module → Immediate update module kia
- **Batch sync**: Reconciliation jobs để ensure data consistency
- **Conflict resolution**: Handle cases khi có conflicting updates
- **Audit logging**: Track tất cả sync activities

---

## 🔐 5. SECURITY & ACCESS CONTROL TÍCH HỢP

### 👥 5.1. Cross-module permissions
**Mô tả**: Phân quyền liên thông giữa 2 module

**Groups**:
- **Asset User**: Tạo đề xuất, mượn tài sản
- **Asset Manager**: Quản lý tài sản, phê duyệt mượn trả
- **Finance User**: Xem báo cáo tài chính
- **Finance Manager**: Phê duyệt mua tài sản, setup accounting
- **System Admin**: Full access cả 2 module

### 🔒 5.2. Record-level security
**Chức năng**:
- **Department-based access**: Chỉ xem tài sản/proposal của department mình
- **Hierarchical approval**: Manager chỉ approve trong phạm vi quyền hạn
- **Financial sensitivity**: Sensitive financial data chỉ finance team access
- **Audit trail protection**: Không ai xóa được audit records

---

## 📱 6. MOBILE & API INTEGRATION

### 📲 6.1. Mobile functions
**Chức năng**:
- **Asset scanning**: Scan QR/barcode để check in/out tài sản
- **Quick borrowing**: Mobile app để tạo đơn mượn nhanh
- **Approval on-the-go**: Approve proposals từ mobile
- **Asset audit**: Mobile form để kiểm kê tài sản

### 🔌 6.2. API integration
**Chức năng**:
- **REST APIs** cho integration với hệ thống khác
- **Webhook notifications** cho real-time events
- **Bulk data import/export** APIs
- **Third-party accounting system** integration

---

## 📊 7. BUSINESS INTELLIGENCE

### 📈 7.1. Advanced analytics
**Chức năng**:
- **Predictive analytics**: Dự báo nhu cầu mua sắm tài sản
- **Usage optimization**: Recommend asset reallocation
- **Cost optimization**: Identify underutilized expensive assets
- **Maintenance forecasting**: Predict maintenance needs

### 🎯 7.2. Performance benchmarking
**Chức năng**:
- **Department comparison**: So sánh efficiency giữa các phòng ban
- **Industry benchmarking**: So với industry standards
- **Time series analysis**: Trend analysis theo thời gian
- **What-if scenarios**: Simulate different allocation strategies

---

# PHẦN IV: TECHNICAL FEATURES

## ⚡ 1. PERFORMANCE OPTIMIZATION

### 🗃️ 1.1. Database optimization
**Chức năng**:
- **Smart indexing**: Indexes trên các fields thường query
- **Data archiving**: Archive old records để maintain performance
- **Query optimization**: Efficient queries cho dashboard & reports
- **Connection pooling**: Optimize database connections

### 📦 1.2. Caching strategy  
**Chức năng**:
- **Dashboard caching**: Cache dashboard metrics
- **Report caching**: Cache generated reports
- **Permission caching**: Cache user permissions
- **Static data caching**: Cache lookup data

---

## 🔧 2. SYSTEM MAINTENANCE

### 🧹 2.1. Data cleanup
**Chức năng**:
- **Old data archival**: Archive data cũ theo retention policy
- **Orphaned record cleanup**: Cleanup records không có liên kết
- **Log rotation**: Rotate system logs để avoid disk full
- **Backup automation**: Automated backup scheduling

### 📊 2.2. Health monitoring
**Chức năng**:
- **System health checks**: Monitor system performance
- **Data integrity checks**: Validate data consistency
- **Error tracking**: Track và analyze errors
- **Performance monitoring**: Monitor response times

---

# KẾT LUẬN

## ✅ TỔNG KẾT CHỨC NĂNG

### Module Quản lý Tài sản (9 nhóm chính):
1. **Dashboard** (2 views)
2. **Quản lý tài sản cơ bản** (3 models chính)  
3. **Quy trình mua tài sản** (1 model, workflow phức tạp)
4. **Mượn trả tài sản** (4 models)
5. **Kiểm kê tài sản** (2 models)
6. **Khấu hao tài sản** (1 model)
7. **Luân chuyển tài sản** (2 models)
8. **Thanh lý tài sản** (1 model)
9. **Lịch sử & theo dõi** (1 model)

### Module Quản lý Tài chính (6 nhóm chính):
1. **Dashboard tài chính** (1 model, nhiều computed fields)
2. **Phê duyệt mua tài sản** (2 models, workflow tích hợp)
3. **Khấu hao tài sản** (3 models)
4. **Kế toán & sổ cái** (2 models)
5. **Báo cáo tài chính** (1 model, templates)
6. **Wizard & utility** (2 models)

### Chức năng tích hợp (7 nhóm):
1. **Tích hợp quy trình mua** (4 sub-processes)
2. **Dashboard tích hợp** (2 types)  
3. **Báo cáo tích hợp** (3 types)
4. **Tự động hóa quy trình** (3 types)
5. **Security & access control** (2 levels)
6. **Mobile & API integration** (2 types)
7. **Business intelligence** (2 types)

## 🎯 ĐIỂM NỔI BẬT

1. **Tính toàn diện**: Coverage toàn bộ asset lifecycle
2. **Tích hợp chặt chẽ**: Seamless integration giữa 2 module  
3. **Automation**: Nhiều quy trình tự động hóa
4. **Flexibility**: Configurable cho nhiều business model
5. **Scalability**: Architecture cho enterprise usage
6. **User Experience**: Intuitive interface & mobile support
7. **Compliance**: Full audit trail & security

**Tổng cộng: 60+ chức năng chính với hàng trăm tính năng phụ**
