# Phân tích Chi tiết Nghiệp vụ Hệ thống

## Tổng quan

Hệ thống gồm 4 module chính hoạt động tích hợp với nhau để quản lý toàn diện tài sản, tài chính và nhân sự của doanh nghiệp.

---

## Module 1: NHÂN SỰ (nhan_su)

### 1.1 Mục đích
Quản lý thông tin nhân viên, cơ cấu tổ chức và lịch sử công tác.

### 1.2 Nghiệp vụ chi tiết

#### NV1.1: Quản lý Nhân viên
| Chức năng | Mô tả |
|-----------|-------|
| Thêm nhân viên | Nhập mã định danh, họ tên, email, SĐT, ngày sinh |
| Sửa thông tin | Cập nhật thông tin cá nhân |
| Xóa nhân viên | Xóa mềm (deactivate) nhân viên đã nghỉ |
| Tìm kiếm | Tìm theo mã, tên, phòng ban |

#### NV1.2: Quản lý Phòng ban
| Chức năng | Mô tả |
|-----------|-------|
| Tạo phòng ban | Nhập mã, tên phòng ban |
| Phân cấp | Thiết lập cấu trúc tổ chức |
| Thống kê | Đếm số nhân viên theo phòng |

#### NV1.3: Quản lý Chức vụ
| Chức năng | Mô tả |
|-----------|-------|
| Tạo chức vụ | Nhập mã, tên chức vụ |
| Phân quyền | Gán quyền hạn theo chức vụ |

#### NV1.4: Lịch sử Công tác
| Chức năng | Mô tả |
|-----------|-------|
| Ghi nhận | Lưu lịch sử thay đổi phòng ban/chức vụ |
| Tra cứu | Xem quá trình công tác của nhân viên |

#### NV1.5: Đăng nhập Web (External App)
| Chức năng | Mô tả |
|-----------|-------|
| Đăng ký | Tạo tài khoản web với username/password |
| Đăng nhập | Xác thực qua API (SHA256 hash) |
| Đổi mật khẩu | Thay đổi mật khẩu web |

---

## Module 2: QUẢN LÝ TÀI SẢN (quan_ly_tai_san)

### 2.1 Mục đích
Quản lý toàn bộ vòng đời tài sản từ mua sắm đến thanh lý.

### 2.2 Nghiệp vụ chi tiết

#### NV2.1: Quản lý Danh mục Tài sản
| Chức năng | Mô tả |
|-----------|-------|
| Tạo danh mục | Phân loại tài sản (Máy tính, Bàn ghế, Xe cộ...) |
| Thống kê | Đếm số tài sản theo danh mục |

#### NV2.2: Quản lý Tài sản
| Chức năng | Mô tả |
|-----------|-------|
| Nhập tài sản | Mã, tên, ngày mua, giá trị, PP khấu hao |
| Theo dõi giá trị | Cập nhật giá trị hiện tại |
| Đính kèm | Upload giấy tờ liên quan |
| Trạng thái | Theo dõi: Đang sử dụng / Đã thanh lý |

#### NV2.3: Phân bổ Tài sản
| Chức năng | Mô tả |
|-----------|-------|
| Phân bổ | Gán tài sản cho phòng ban/nhân viên |
| Theo dõi vị trí | Biết tài sản đang ở đâu |
| Tình trạng | Bình thường / Hỏng / Mất |
| Lịch sử | Xem lịch sử phân bổ |

#### NV2.4: Đơn mượn Tài sản
| Chức năng | Mô tả |
|-----------|-------|
| Tạo đơn | Nhân viên tạo đơn mượn tài sản |
| Chọn tài sản | Chọn từ danh sách tài sản khả dụng |
| Thời gian | Đặt thời gian mượn/trả dự kiến |
| Lý do | Ghi lý do mượn |

#### NV2.5: Duyệt Đơn mượn
| Chức năng | Mô tả |
|-----------|-------|
| Xem đơn | Quản lý xem danh sách đơn chờ duyệt |
| Duyệt | Phê duyệt đơn mượn |
| Từ chối | Từ chối với lý do |
| Giao tài sản | Xác nhận đã giao tài sản |

#### NV2.6: Trả Tài sản
| Chức năng | Mô tả |
|-----------|-------|
| Nhận trả | Xác nhận nhận lại tài sản |
| Kiểm tra | Đánh giá tình trạng sau khi trả |
| Hoàn tất | Đóng đơn mượn |

#### NV2.7: Kiểm kê Tài sản
| Chức năng | Mô tả |
|-----------|-------|
| Tạo đợt kiểm kê | Theo phòng ban, theo thời gian |
| Thực kiểm | So sánh thực tế với sổ sách |
| Báo cáo | Lập biên bản kiểm kê |

#### NV2.8: Luân chuyển Tài sản
| Chức năng | Mô tả |
|-----------|-------|
| Tạo lệnh | Chuyển tài sản giữa các phòng ban |
| Phê duyệt | Duyệt lệnh luân chuyển |
| Thực hiện | Xác nhận đã chuyển |

#### NV2.9: Thanh lý Tài sản
| Chức năng | Mô tả |
|-----------|-------|
| Đề xuất | Đề xuất thanh lý tài sản cũ/hỏng |
| Định giá | Xác định giá thanh lý |
| Phê duyệt | Duyệt thanh lý |
| Thực hiện | Ghi nhận thanh lý, cập nhật trạng thái |

#### NV2.10: Đề xuất Mua Tài sản
| Chức năng | Mô tả |
|-----------|-------|
| Tạo đề xuất | Nhân viên/phòng ban đề xuất mua mới |
| Chi tiết | Liệt kê thiết bị cần mua, số lượng, giá |
| Gửi duyệt | Gửi lên cấp trên phê duyệt |

---

## Module 3: QUẢN LÝ TÀI CHÍNH (quan_ly_tai_chinh)

### 3.1 Mục đích
Quản lý khấu hao, phê duyệt mua sắm, bút toán kế toán và báo cáo tài chính.

### 3.2 Nghiệp vụ chi tiết

#### NV3.1: Phê duyệt Mua Tài sản
| Chức năng | Mô tả |
|-----------|-------|
| Tiếp nhận | Nhận đề xuất từ module Tài sản |
| Xem xét | Kiểm tra ngân sách, tính cần thiết |
| Phê duyệt | Duyệt hoặc từ chối với ghi chú |
| Tạo tài sản | Sau duyệt, tự động tạo tài sản mới |

#### NV3.2: Quản lý Khấu hao
| Chức năng | Mô tả |
|-----------|-------|
| Thiết lập | Cấu hình PP khấu hao (đường thẳng/giảm dần) |
| Tính toán | Tự động tính khấu hao hàng năm |
| Theo dõi | Giám sát giá trị còn lại |
| Hoàn thành | Đánh dấu khi khấu hao hết |

#### NV3.3: Bút toán Kế toán
| Chức năng | Mô tả |
|-----------|-------|
| Tạo bút toán | Ghi nhận Nợ/Có |
| Liên kết | Gắn với khấu hao hoặc phê duyệt mua |
| Duyệt | Xác nhận bút toán |
| Sổ cái | Tổng hợp vào sổ kế toán |

#### NV3.4: Báo cáo Tài chính
| Chức năng | Mô tả |
|-----------|-------|
| Tạo báo cáo | Báo cáo theo tháng/quý/năm |
| Nội dung | Doanh thu, chi phí, lợi nhuận |
| Chi tiết | Phân tích chi phí khấu hao, lương, văn phòng |
| Xuất | Export PDF/Excel |

#### NV3.5: Dashboard Tài chính
| Chức năng | Mô tả |
|-----------|-------|
| Tổng quan | Hiển thị các chỉ số tài chính |
| Biểu đồ | Xu hướng khấu hao, mua sắm |
| Phân bổ | Biểu đồ phân bổ theo phòng ban |

---

## Module 4: TRANG CHỦ & CHATBOT (q_trang_chu)

### 4.1 Mục đích
Cung cấp giao diện dashboard tổng quan và AI Chatbot hỗ trợ người dùng.

### 4.2 Nghiệp vụ chi tiết

#### NV4.1: Dashboard Tổng quan
| Chức năng | Mô tả |
|-----------|-------|
| Thống kê | Tổng tài sản, giá trị, đơn mượn |
| Widget | Các widget hiển thị nhanh |
| Cập nhật | Real-time data |

#### NV4.2: AI Chatbot
| Chức năng | Mô tả |
|-----------|-------|
| Hỏi đáp | Trả lời câu hỏi về tài sản, quy trình |
| Intent | Nhận diện ý định người dùng |
| Context | Truy vấn dữ liệu thực từ hệ thống |
| AI | Sử dụng Google Gemini để phản hồi |

#### NV4.3: Knowledge Base
| Chức năng | Mô tả |
|-----------|-------|
| FAQ | Câu hỏi thường gặp |
| Kiến thức | Bài viết hướng dẫn |
| Quy định | Chính sách công ty |

#### NV4.4: Quản lý Hội thoại
| Chức năng | Mô tả |
|-----------|-------|
| Lưu trữ | Lưu lịch sử chat theo user |
| Tra cứu | Xem lại các cuộc hội thoại |

---

## Nghiệp vụ Kết hợp giữa các Module

### KH1: Quy trình Mua sắm Tài sản

```
[Nhân sự] ──► [Tài sản] ──► [Tài chính]

1. Nhân viên (Nhân sự) tạo đề xuất mua
2. Đề xuất được gửi → Module Tài sản
3. Module Tài chính phê duyệt
4. Sau duyệt → Tạo tài sản mới
5. Tự động tạo lịch khấu hao
6. Phân bổ cho nhân viên/phòng ban
```

### KH2: Quy trình Mượn trả Tài sản

```
[Nhân sự] ◄──► [Tài sản]

1. Nhân viên (Nhân sự) tạo đơn mượn
2. Chọn tài sản từ phân bổ khả dụng
3. Quản lý phòng ban duyệt
4. Nhân viên nhận tài sản
5. Trả tài sản, kiểm tra tình trạng
6. Cập nhật phân bổ
```

### KH3: Quy trình Thanh lý + Bút toán

```
[Tài sản] ──► [Tài chính]

1. Đề xuất thanh lý tài sản
2. Định giá thanh lý
3. Phê duyệt thanh lý
4. Tạo bút toán ghi nhận
5. Cập nhật trạng thái tài sản
6. Cập nhật sổ kế toán
```

### KH4: Chatbot truy vấn đa Module

```
[Chatbot] ──► [Nhân sự] + [Tài sản] + [Tài chính]

User: "Tôi đang mượn những tài sản nào?"
1. Chatbot nhận diện intent: muon_tai_san
2. Lấy user_id → Tìm nhan_vien tương ứng
3. Truy vấn đơn mượn đang hoạt động
4. Trả về danh sách tài sản đang mượn
```

### KH5: Dashboard tổng hợp

```
[Dashboard] ◄── [Nhân sự] + [Tài sản] + [Tài chính]

Dashboard hiển thị:
- Số nhân viên (từ Nhân sự)
- Tổng tài sản, giá trị (từ Tài sản)
- Chi phí khấu hao (từ Tài chính)
- Đơn mượn chờ duyệt (từ Tài sản)
```

### KH6: Báo cáo Tài sản theo Phòng ban

```
[Tài chính] ◄── [Tài sản] ◄── [Nhân sự]

1. Lấy danh sách phòng ban (Nhân sự)
2. Lấy phân bổ tài sản theo phòng (Tài sản)
3. Tính giá trị, khấu hao (Tài chính)
4. Tạo báo cáo phân bổ theo phòng ban
```

---

## Ma trận Quan hệ Module

| Module | Nhân sự | Tài sản | Tài chính | Trang chủ |
|--------|---------|---------|-----------|-----------|
| **Nhân sự** | - | Phân bổ, Mượn | Phê duyệt | Chatbot |
| **Tài sản** | NV sử dụng | - | Khấu hao | Dashboard |
| **Tài chính** | - | Giá trị TS | - | Dashboard |
| **Trang chủ** | Query | Query | Query | - |

---

## Tổng kết

| Module | Số nghiệp vụ | Bảng dữ liệu |
|--------|-------------|--------------|
| Nhân sự | 5 | 4 |
| Tài sản | 10 | 11 |
| Tài chính | 5 | 6 |
| Trang chủ | 4 | 12 |
| Kết hợp | 6 | - |
| **Tổng** | **30** | **33** |
