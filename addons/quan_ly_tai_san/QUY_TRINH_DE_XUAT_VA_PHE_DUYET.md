# QUY TRÌNH ĐỀ XUẤT VÀ PHÊ DUYỆT MUA TÀI SẢN

## 📋 Tổng quan

Hệ thống quản lý đề xuất mua tài sản được thiết kế với **quy trình 2 bước** để đảm bảo kiểm soát tài chính:

1. **Bước 1**: Tạo đề xuất tại module **Quản lý Tài sản** 
2. **Bước 2**: Phê duyệt tại module **Quản lý Tài chính**

---

## 🔐 NGUYÊN TẮC QUAN TRỌNG

> ⚠️ **LƯU Ý**: Module **Quản lý Tài sản** CHỈ được phép:
> - ✅ Tạo đề xuất mua tài sản
> - ✅ Gửi đề xuất để phê duyệt
> - ❌ **KHÔNG** được phép tự phê duyệt đề xuất

> ✔️ **Phê duyệt** chỉ được thực hiện tại module **Quản lý Tài chính**

---

## 📝 QUY TRÌNH CHI TIẾT

### BƯỚC 1: Tạo đề xuất (Module: Quản lý Tài sản)

**Vị trí**: Menu `Tài sản` → `Đề xuất mua tài sản`

1. **Tạo đề xuất mới**:
   - Nhập thông tin cơ bản:
     - Tiêu đề đề xuất
     - Ngày đề xuất
     - Người đề xuất (tự động)
     - Phòng ban
     - Ngày dự kiến nhận hàng

2. **Thêm chi tiết thiết bị**:
   - Tên thiết bị
   - Danh mục tài sản
   - Số lượng, đơn giá
   - Phương pháp khấu hao
   - Nhà cung cấp đề xuất

3. **Nhập thông tin bổ sung**:
   - Lý do đề xuất (bắt buộc)
   - Mô tả chi tiết
   - File đính kèm (báo giá, hình ảnh...)

4. **Lưu đề xuất** → Trạng thái: `Nháp`

### BƯỚC 2: Gửi đề xuất (Module: Quản lý Tài sản)

1. Kiểm tra lại thông tin đề xuất
2. Nhấn nút **"Gửi đề xuất"**
3. Hệ thống tự động:
   - Chuyển trạng thái: `Đã gửi` → `Chờ phê duyệt tài chính`
   - Tạo đơn phê duyệt ở module **Quản lý Tài chính**
   - Gửi thông báo cho bộ phận tài chính

### BƯỚC 3: Phê duyệt (Module: Quản lý Tài chính)

> 🔒 **Quan trọng**: Bước này CHỈ thực hiện tại module **Quản lý Tài chính**

**Vị trí**: Menu `Tài chính` → `Phê duyệt mua tài sản`

1. **Người có quyền phê duyệt** truy cập đơn phê duyệt
2. **Kiểm tra thông tin**:
   - Chi tiết đề xuất
   - Thông tin thiết bị
   - Tổng giá trị

3. **Cấu hình tài khoản kế toán**:
   - Tài khoản tài sản cố định (VD: 211)
   - Tài khoản nguồn vốn (VD: 112, 1121)
   - Sổ nhật ký

4. **Quyết định phê duyệt**:
   - Nhấn **"Phê duyệt"**: Hệ thống tự động:
     - Tạo tài sản trong module Quản lý Tài sản
     - Ghi nhận bút toán kế toán
     - Tạo lịch khấu hao
     - Cập nhật trạng thái đề xuất gốc: `Đã phê duyệt`
   
   - Nhấn **"Từ chối"**: 
     - Cập nhật trạng thái: `Từ chối`
     - Gửi thông báo về người đề xuất

### BƯỚC 4: Theo dõi kết quả (Module: Quản lý Tài sản)

Sau khi phê duyệt, quay lại đề xuất gốc để:
- Xem trạng thái: `Đã phê duyệt`
- Nhấn **"Xem tài sản"** để xem tài sản đã được tạo
- Nhấn **"Xem đơn phê duyệt"** để xem chi tiết phê duyệt tài chính

---

## 🛡️ CƠ CHẾ BẢO VỆ

Hệ thống áp dụng nhiều lớp bảo vệ để đảm bảo quy trình:

### 1. Ràng buộc Code (Code Constraints)
- **Không cho phép** thay đổi trạng thái trực tiếp sang `approved` hoặc `rejected`
- Chỉ callback từ module tài chính mới được phép cập nhật trạng thái này

```python
# Nếu cố gắng tự phê duyệt sẽ nhận lỗi:
UserError: KHÔNG THỂ TỰ PHÊ DUYỆT ĐỀ XUẤT!

Đề xuất mua tài sản chỉ có thể được phê duyệt thông qua 
module Quản lý Tài chính.

Vui lòng truy cập menu: Tài chính > Phê duyệt mua tài sản 
để thực hiện phê duyệt.
```

### 2. Quy tắc bảo mật (Security Rules)
- Record rules kiểm soát quyền đọc/ghi
- Người dùng thường chỉ được:
  - Chỉnh sửa đề xuất ở trạng thái `draft`, `submitted`, `waiting_approval`
  - KHÔNG được chỉnh sửa đề xuất ở trạng thái `approved`, `rejected` (trừ admin)

### 3. Giao diện người dùng (UI)
- Không có button "Phê duyệt" trên form đề xuất
- Có cảnh báo rõ ràng về quy trình phê duyệt
- Smart button để chuyển đến module tài chính

---

## ❓ CÂU HỎI THƯỜNG GẶP

### Q1: Tại sao tôi không thể phê duyệt đề xuất của mình?
**A**: Đây là thiết kế có chủ đích để đảm bảo kiểm soát tài chính. Mọi đề xuất mua tài sản phải được bộ phận tài chính phê duyệt tại module **Quản lý Tài chính**.

### Q2: Làm sao biết đề xuất của tôi đã được phê duyệt?
**A**: Bạn sẽ nhận được thông báo và có thể:
- Kiểm tra trạng thái đề xuất (sẽ hiển thị `Đã phê duyệt`)
- Xem trong Chatter (Activity/Messages)
- Nhấn nút "Xem tài sản" để xem tài sản đã được tạo

### Q3: Nếu đề xuất bị từ chối thì sao?
**A**: Bạn có thể:
- Xem lý do từ chối trong ghi chú phê duyệt
- Nhấn **"Đưa về nháp"** để chỉnh sửa
- Cập nhật thông tin và gửi lại

### Q4: Ai có quyền phê duyệt?
**A**: Chỉ những người dùng có quyền trong module **Quản lý Tài chính** mới có thể phê duyệt. Liên hệ quản trị viên hệ thống để được cấp quyền.

### Q5: Tôi là admin, tôi có thể tự phê duyệt không?
**A**: Ngay cả admin cũng nên tuân theo quy trình. Tuy nhiên, admin có thể:
- Truy cập module Quản lý Tài chính để phê duyệt
- Hoặc sử dụng quyền đặc biệt để bypass (không khuyến khích)

---

## 📊 SƠ ĐỒ QUY TRÌNH

```
┌─────────────────────────────────────────────────────────────┐
│         MODULE: QUẢN LÝ TÀI SẢN                             │
├─────────────────────────────────────────────────────────────┤
│  1. Tạo đề xuất mua tài sản                                 │
│     - Nhập thông tin thiết bị                               │
│     - Lý do, mô tả                                          │
│     - File đính kèm                                         │
│                                                             │
│  2. Gửi đề xuất                                             │
│     ↓                                                       │
│     Trạng thái: Nháp → Đã gửi → Chờ phê duyệt             │
└─────────────────────────────────────────────────────────────┘
                          ↓
              Tự động tạo đơn phê duyệt
                          ↓
┌─────────────────────────────────────────────────────────────┐
│         MODULE: QUẢN LÝ TÀI CHÍNH                           │
├─────────────────────────────────────────────────────────────┤
│  3. Xem đơn phê duyệt                                       │
│     - Kiểm tra thông tin                                    │
│     - Cấu hình tài khoản kế toán                            │
│                                                             │
│  4. Phê duyệt / Từ chối                                     │
│     ↓                                                       │
│  Nếu PHÊ DUYỆT:                                             │
│     - Tạo tài sản tự động                                   │
│     - Ghi nhận bút toán                                     │
│     - Tạo lịch khấu hao                                     │
│     - Cập nhật trạng thái đề xuất → Đã phê duyệt           │
│                                                             │
│  Nếu TỪ CHỐI:                                               │
│     - Cập nhật trạng thái → Từ chối                         │
│     - Thông báo người đề xuất                               │
└─────────────────────────────────────────────────────────────┘
                          ↓
              Cập nhật callback về đề xuất gốc
                          ↓
┌─────────────────────────────────────────────────────────────┐
│         MODULE: QUẢN LÝ TÀI SẢN                             │
├─────────────────────────────────────────────────────────────┤
│  5. Xem kết quả                                             │
│     - Trạng thái: Đã phê duyệt / Từ chối                   │
│     - Xem tài sản đã tạo (nếu được duyệt)                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 HỖ TRỢ KỸ THUẬT

Nếu gặp vấn đề hoặc cần hỗ trợ, vui lòng liên hệ:
- Email: support@company.com
- Quản trị viên hệ thống

---

**Phiên bản**: 1.0  
**Cập nhật**: Tháng 1/2026  
**Tác giả**: Nguyễn Ngọc Đan Trường
