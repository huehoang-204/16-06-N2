# CHƯƠNG 3: PHÂN TÍCH, THIẾT KẾ VÀ TRIỂN KHAI HỆ THỐNG

---

## MỤC LỤC CHƯƠNG 3

- 3.1. Tổng quan hệ thống
- 3.2. Phân tích yêu cầu hệ thống
- 3.3. Thiết kế cơ sở dữ liệu
- 3.4. Thiết kế luồng nghiệp vụ
- 3.5. Thiết kế giao diện người dùng
- 3.6. Triển khai hệ thống
- 3.7. Tích hợp 2 Module
- 3.8. Đánh giá và kết luận

---

## 3.1. TỔNG QUAN HỆ THỐNG

### 3.1.1. Giới thiệu

Hệ thống Quản lý Tài sản và Tài chính được xây dựng trên nền tảng Odoo 15, bao gồm hai module tích hợp chặt chẽ:


| STT | Module                | Mô tả                                                      |
| --- | --------------------- | ------------------------------------------------------------ |
| 1   | **quan_ly_tai_san**   | Quản lý toàn bộ vòng đời tài sản của doanh nghiệp |
| 2   | **quan_ly_tai_chinh** | Quản lý phê duyệt mua sắm và ghi nhận tài chính     |

### 3.1.2. Kiến trúc tổng thể hệ thống

**[HÌNH 3.1: Sơ đồ kiến trúc tổng thể hệ thống - Chèn hình ảnh tại đây]**

Hệ thống được thiết kế theo mô hình MVC (Model-View-Controller) của Odoo với các thành phần chính:


| Thành phần   | Mô tả                                         | Công nghệ      |
| -------------- | ----------------------------------------------- | ---------------- |
| **Model**      | Xử lý logic nghiệp vụ và tương tác CSDL | Python, ORM Odoo |
| **View**       | Giao diện người dùng                        | XML, QWeb, OWL   |
| **Controller** | Điều khiển luồng xử lý                    | Python           |
| **Database**   | Lưu trữ dữ liệu                             | PostgreSQL       |

### 3.1.3. Các module phụ thuộc

```
quan_ly_tai_san
├── base
├── web
├── nhan_su
├── hr
└── account

quan_ly_tai_chinh
├── base
├── quan_ly_tai_san  ← Phụ thuộc vào module tài sản
├── nhan_su
├── hr
└── account
```

---

## 3.2. PHÂN TÍCH YÊU CẦU HỆ THỐNG

### 3.2.1. Yêu cầu chức năng

#### A. Module Quản lý Tài sản (quan_ly_tai_san)


| STT | Nhóm chức năng             | Mô tả chi tiết                                                |
| --- | ----------------------------- | ---------------------------------------------------------------- |
| 1   | Dashboard tổng quan          | Hiển thị thống kê tài sản, giá trị, biểu đồ phân bổ |
| 2   | Quản lý danh mục tài sản | Tạo/sửa/xóa loại tài sản, tự động tính số lượng     |
| 3   | Quản lý tài sản cụ thể  | Thông tin chi tiết, khấu hao, trạng thái, lịch sử         |
| 4   | Phân bổ tài sản           | Gán tài sản cho phòng ban/nhân viên                        |
| 5   | Đề xuất mua tài sản      | Tạo đề xuất, gửi phê duyệt, theo dõi trạng thái        |
| 6   | Mượn/trả tài sản         | Tạo đơn mượn, phê duyệt, theo dõi hạn trả              |
| 7   | Kiểm kê tài sản           | Tạo phiếu kiểm kê, ghi nhận tình trạng                    |
| 8   | Luân chuyển tài sản       | Chuyển tài sản giữa các phòng ban                          |
| 9   | Thanh lý tài sản           | Bán hoặc tiêu hủy tài sản                                  |

#### B. Module Quản lý Tài chính (quan_ly_tai_chinh)


| STT | Nhóm chức năng         | Mô tả chi tiết                                          |
| --- | ------------------------- | ---------------------------------------------------------- |
| 1   | Dashboard tài chính     | Thống kê phê duyệt, khấu hao, bút toán, KPI         |
| 2   | Phê duyệt mua tài sản | Xem xét đề xuất, phê duyệt/từ chối, tạo tài sản |
| 3   | Khấu hao tài sản       | Thiết lập và quản lý lịch khấu hao                  |
| 4   | Bút toán kế toán      | Ghi nhận các nghiệp vụ kế toán                       |
| 5   | Tài khoản quản trị    | Quản lý hệ thống tài khoản                           |
| 6   | Báo cáo tài chính     | Các báo cáo tài chính định kỳ                      |

### 3.2.2. Yêu cầu phi chức năng


| STT | Yêu cầu   | Mô tả                                                           |
| --- | ----------- | ----------------------------------------------------------------- |
| 1   | Hiệu năng | Phản hồi trong vòng 3 giây cho các thao tác thông thường |
| 2   | Bảo mật   | Phân quyền theo vai trò, audit log đầy đủ                  |
| 3   | Khả dụng  | Hệ thống hoạt động 24/7 với uptime > 99%                    |
| 4   | Mở rộng   | Hỗ trợ mở rộng module và tùy chỉnh                         |
| 5   | Tích hợp  | API để tích hợp với hệ thống khác                         |

### 3.2.3. Các tác nhân hệ thống (Actors)


| Actor                     | Vai trò               | Quyền hạn chính                                                |
| ------------------------- | ---------------------- | ----------------------------------------------------------------- |
| **Nhân viên**           | Người dùng cuối    | Tạo đề xuất mua, mượn tài sản, xem tài sản được gán |
| **Quản lý tài sản**   | Quản trị tài sản   | CRUD tài sản, phân bổ, kiểm kê, thanh lý                   |
| **Quản lý tài chính** | Quản trị tài chính | Phê duyệt mua, ghi nhận kế toán, báo cáo                   |
| **Admin**                 | Quản trị hệ thống  | Toàn quyền trên cả 2 module                                   |

**[HÌNH 3.2: Sơ đồ Use Case tổng quát - Chèn hình ảnh tại đây]**

---

## 3.3. THIẾT KẾ CƠ SỞ DỮ LIỆU

### 3.3.1. Sơ đồ quan hệ thực thể (ERD)

**[HÌNH 3.3: Sơ đồ ERD tổng quan - Chèn hình ảnh tại đây]**

### 3.3.2. Chi tiết các bảng dữ liệu - Module Quản lý Tài sản

#### Bảng 3.1: danh_muc_tai_san (Danh mục tài sản)


| STT | Tên trường     | Kiểu dữ liệu | Ràng buộc      | Mô tả                                               |
| --- | ----------------- | --------------- | ---------------- | ----------------------------------------------------- |
| 1   | id                | Integer         | PK, Auto         | Khóa chính, tự động tăng                        |
| 2   | ma_danh_muc_ts    | Char            | Unique, Required | Mã loại tài sản (VD: DMTS001)                     |
| 3   | ten_danh_muc_ts   | Char            | Required         | Tên loại tài sản (VD: Máy tính)                 |
| 4   | mo_ta_danh_muc_ts | Char            | -                | Mô tả chi tiết về loại tài sản                 |
| 5   | so_luong_tong     | Integer         | Computed         | Số lượng tài sản thuộc loại (tự động tính) |

---

#### Bảng 3.2: tai_san (Tài sản)


| STT | Tên trường            | Kiểu dữ liệu | Ràng buộc            | Mô tả                                                   |
| --- | ------------------------ | --------------- | ---------------------- | --------------------------------------------------------- |
| 1   | id                       | Integer         | PK, Auto               | Khóa chính, tự động tăng                            |
| 2   | ma_tai_san               | Char            | Unique, Required       | Mã tài sản (VD: TS-00001)                              |
| 3   | ten_tai_san              | Char            | Required               | Tên tài sản (VD: Laptop Dell XPS)                      |
| 4   | ngay_mua_ts              | Date            | Required               | Ngày mua tài sản                                       |
| 5   | don_vi_tien_te           | Selection       | Required               | Đơn vị tiền: 'vnd' hoặc 'usd'                        |
| 6   | gia_tri_ban_dau          | Float           | Required               | Giá trị ban đầu khi mua                               |
| 7   | gia_tri_hien_tai         | Float           | Required               | Giá trị còn lại sau khấu hao                         |
| 8   | danh_muc_ts_id           | Many2one        | FK → danh_muc_tai_san | Liên kết đến danh mục tài sản                      |
| 9   | giay_to_tai_san          | Binary          | -                      | File đính kèm (hóa đơn, bảo hành...)              |
| 10  | giay_to_tai_san_filename | Char            | -                      | Tên file đính kèm                                     |
| 11  | hinh_anh                 | Image           | -                      | Hình ảnh tài sản (max 200x200px)                      |
| 12  | pp_khau_hao              | Selection       | Required               | Phương pháp: 'straight-line', 'degressive', 'none'     |
| 13  | thoi_gian_su_dung        | Integer         | -                      | Thời gian đã sử dụng (năm)                          |
| 14  | thoi_gian_toi_da         | Integer         | -                      | Thời gian sử dụng tối đa (năm)                      |
| 15  | ty_le_khau_hao           | Float           | -                      | Tỷ lệ khấu hao (%) cho phương pháp giảm dần       |
| 16  | don_vi_tinh              | Char            | Required               | Đơn vị tính (VD: Chiếc, Bộ)                         |
| 17  | ghi_chu                  | Text            | -                      | Ghi chú thêm                                            |
| 18  | trang_thai_thanh_ly      | Selection       | Computed               | Trạng thái: 'chua_phan_bo', 'da_phan_bo', 'da_thanh_ly' |

---

#### Bảng 3.3: phan_bo_tai_san (Phân bổ tài sản)


| STT | Tên trường        | Kiểu dữ liệu | Ràng buộc             | Mô tả                                      |
| --- | -------------------- | --------------- | ----------------------- | -------------------------------------------- |
| 1   | id                   | Integer         | PK, Auto                | Khóa chính, tự động tăng               |
| 2   | phong_ban_id         | Many2one        | FK → phong_ban         | Phòng ban được gán tài sản            |
| 3   | tai_san_id           | Many2one        | FK → tai_san, Required | Tài sản được phân bổ                  |
| 4   | ngay_phat            | Date            | Required                | Ngày phân bổ tài sản                    |
| 5   | nhan_vien_su_dung_id | Many2one        | FK → nhan_vien         | Nhân viên sử dụng cụ thể               |
| 6   | ghi_chu              | Char            | -                       | Ghi chú phân bổ                           |
| 7   | trang_thai           | Selection       | Required                | 'in-use' hoặc 'not-in-use'                  |
| 8   | tinh_trang           | Selection       | -                       | 'binh_thuong', 'dang_muon', 'hu_hong', 'mat' |
| 9   | vi_tri_tai_san_id    | Many2one        | FK → phong_ban         | Vị trí thực tế của tài sản            |

---

#### Bảng 3.4: de_xuat_mua_tai_san (Đề xuất mua tài sản)


| STT | Tên trường     | Kiểu dữ liệu | Ràng buộc                 | Mô tả                                     |
| --- | ----------------- | --------------- | --------------------------- | ------------------------------------------- |
| 1   | id                | Integer         | PK, Auto                    | Khóa chính, tự động tăng              |
| 2   | ma_de_xuat        | Char            | Unique, Required            | Mã đề xuất tự động (VD: DXMTS-00001) |
| 3   | ten_de_xuat       | Char            | Required                    | Tiêu đề đề xuất                       |
| 4   | ngay_de_xuat      | Date            | Required                    | Ngày tạo đề xuất                       |
| 5   | nguoi_de_xuat_id  | Many2one        | FK → res.users             | Người tạo đề xuất                     |
| 6   | phong_ban_id      | Many2one        | FK → phong_ban             | Phòng ban đề xuất                       |
| 7   | tong_gia_tri      | Float           | Computed                    | Tổng giá trị các thiết bị             |
| 8   | don_vi_tien_te    | Selection       | Required                    | 'vnd' hoặc 'usd'                           |
| 9   | ly_do             | Text            | Required                    | Lý do đề xuất mua                       |
| 10  | mo_ta             | Html            | -                           | Mô tả chi tiết (rich text)               |
| 11  | state             | Selection       | Required                    | Trạng thái workflow                       |
| 12  | ngay_du_kien_nhan | Date            | -                           | Ngày dự kiến nhận hàng                 |
| 13  | phe_duyet_id      | Many2one        | FK → phe_duyet_mua_tai_san | Liên kết đơn phê duyệt                |
| 14  | tai_san_ids       | Many2many       | -                           | Danh sách tài sản được tạo           |
| 15  | ghi_chu           | Text            | -                           | Ghi chú thêm                              |

**Các giá trị State:**

- `draft`: Nháp
- `submitted`: Đã gửi
- `waiting_approval`: Chờ phê duyệt tài chính
- `approved`: Đã phê duyệt
- `rejected`: Từ chối
- `cancelled`: Đã hủy

---

#### Bảng 3.5: de_xuat_mua_tai_san_line (Chi tiết đề xuất mua)


| STT | Tên trường     | Kiểu dữ liệu | Ràng buộc               | Mô tả                                  |
| --- | ----------------- | --------------- | ------------------------- | ---------------------------------------- |
| 1   | id                | Integer         | PK, Auto                  | Khóa chính, tự động tăng           |
| 2   | de_xuat_id        | Many2one        | FK → de_xuat_mua_tai_san | Đề xuất cha                           |
| 3   | ten_thiet_bi      | Char            | Required                  | Tên thiết bị cần mua                 |
| 4   | danh_muc_ts_id    | Many2one        | FK → danh_muc_tai_san    | Danh mục tài sản                      |
| 5   | mo_ta             | Text            | -                         | Mô tả chi tiết                        |
| 6   | thong_so_ky_thuat | Text            | -                         | Thông số kỹ thuật                    |
| 7   | so_luong          | Integer         | Required                  | Số lượng cần mua                     |
| 8   | don_vi_tinh       | Char            | -                         | Đơn vị tính                          |
| 9   | don_gia           | Float           | Required                  | Đơn giá                               |
| 10  | thanh_tien        | Float           | Computed                  | Thành tiền = số lượng × đơn giá |
| 11  | pp_khau_hao       | Selection       | -                         | Phương pháp khấu hao dự kiến       |
| 12  | thoi_gian_su_dung | Integer         | -                         | Thời gian sử dụng dự kiến (năm)    |
| 13  | ty_le_khau_hao    | Float           | -                         | Tỷ lệ khấu hao (%)                    |
| 14  | nha_cung_cap      | Char            | -                         | Nhà cung cấp đề xuất                |

---

#### Bảng 3.6: don_muon_tai_san (Đơn mượn tài sản)


| STT | Tên trường         | Kiểu dữ liệu | Ràng buộc               | Mô tả                             |
| --- | --------------------- | --------------- | ------------------------- | ----------------------------------- |
| 1   | id                    | Integer         | PK, Auto                  | Khóa chính, tự động tăng      |
| 2   | ma_don_muon           | Char            | Unique, Required          | Mã đơn mượn (VD: DMTS-00001)   |
| 3   | ten_don_muon          | Char            | Required                  | Tên/tiêu đề đơn mượn        |
| 4   | phong_ban_cho_muon_id | Many2one        | FK → phong_ban, Required | Phòng ban có tài sản cho mượn |
| 5   | thoi_gian_muon        | Datetime        | Required                  | Thời điểm bắt đầu mượn      |
| 6   | thoi_gian_tra         | Datetime        | Required                  | Thời điểm dự kiến trả         |
| 7   | nhan_vien_muon_id     | Many2one        | FK → nhan_vien, Required | Nhân viên xin mượn              |
| 8   | ly_do_muon            | Text            | -                         | Lý do mượn tài sản             |
| 9   | trang_thai            | Selection       | Required                  | 'dang-cho', 'da-duyet', 'tu-choi'   |
| 10  | ghi_chu               | Char            | -                         | Ghi chú                            |

---

#### Bảng 3.7: muon_tra_tai_san (Phiếu mượn trả tài sản)


| STT | Tên trường         | Kiểu dữ liệu | Ràng buộc               | Mô tả                                                    |
| --- | --------------------- | --------------- | ------------------------- | ---------------------------------------------------------- |
| 1   | id                    | Integer         | PK, Auto                  | Khóa chính, tự động tăng                             |
| 2   | ma_phieu_muon_tra     | Char            | Unique, Required          | Mã phiếu mượn trả                                     |
| 3   | ten_phieu_muon_tra    | Char            | Required                  | Tên phiếu                                                |
| 4   | ma_don_muon_id        | Many2one        | FK → don_muon_tai_san    | Đơn mượn gốc                                          |
| 5   | phong_ban_cho_muon_id | Many2one        | FK → phong_ban, Required | Phòng ban cho mượn                                      |
| 6   | thoi_gian_muon        | Datetime        | Required                  | Thời gian mượn thực tế                                |
| 7   | thoi_gian_tra         | Datetime        | Required                  | Thời gian trả dự kiến                                  |
| 8   | nhan_vien_muon_id     | Many2one        | FK → nhan_vien, Required | Nhân viên mượn                                         |
| 9   | trang_thai            | Selection       | Required                  | 'dang-muon' hoặc 'da-tra'                                 |
| 10  | tinh_trang            | Char            | Computed                  | Tình trạng hiện tại (Đang mượn/Quá hạn/Đã trả) |
| 11  | ghi_chu               | Char            | -                         | Ghi chú                                                   |

---

#### Bảng 3.8: kiem_ke_tai_san (Kiểm kê tài sản)


| STT | Tên trường        | Kiểu dữ liệu | Ràng buộc      | Mô tả                                  |
| --- | -------------------- | --------------- | ---------------- | ---------------------------------------- |
| 1   | id                   | Integer         | PK, Auto         | Khóa chính, tự động tăng           |
| 2   | ma_phieu_kiem_ke     | Char            | Unique, Required | Mã phiếu kiểm kê                     |
| 3   | ten_phieu_kiem_ke    | Char            | Required         | Tên phiếu kiểm kê                    |
| 4   | phong_ban_id         | Many2one        | FK → phong_ban  | Phòng ban cần kiểm kê                |
| 5   | nhan_vien_kiem_ke_id | Many2one        | FK → nhan_vien  | Nhân viên thực hiện                  |
| 6   | thoi_gian_tao        | Datetime        | Required         | Thời gian tạo phiếu                   |
| 7   | ghi_chu              | Char            | -                | Ghi chú                                 |
| 8   | trang_thai_phieu     | Char            | Computed         | 'Chưa kiểm kê' hoặc 'Đã kiểm kê' |

---

#### Bảng 3.9: kiem_ke_tai_san_line (Chi tiết kiểm kê)


| STT | Tên trường      | Kiểu dữ liệu | Ràng buộc           | Mô tả                        |
| --- | ------------------ | --------------- | --------------------- | ------------------------------ |
| 1   | id                 | Integer         | PK, Auto              | Khóa chính, tự động tăng |
| 2   | kiem_ke_tai_san_id | Many2one        | FK → kiem_ke_tai_san | Phiếu kiểm kê cha           |
| 3   | phan_bo_tai_san_id | Many2one        | FK → phan_bo_tai_san | Tài sản được kiểm kê    |
| 4   | trang_thai         | Selection       | Required              | 'in-progress' hoặc 'finished' |
| 5   | ket_qua            | Selection       | -                     | 'ton-tai', 'thieu', 'hong'     |
| 6   | ghi_chu            | Text            | -                     | Ghi chú tình trạng          |

---

#### Bảng 3.10: luan_chuyen_tai_san (Luân chuyển tài sản)


| STT | Tên trường         | Kiểu dữ liệu | Ràng buộc      | Mô tả                        |
| --- | --------------------- | --------------- | ---------------- | ------------------------------ |
| 1   | id                    | Integer         | PK, Auto         | Khóa chính, tự động tăng |
| 2   | ma_phieu_luan_chuyen  | Char            | Unique, Required | Mã phiếu luân chuyển       |
| 3   | bo_phan_nguon         | Many2one        | FK → phong_ban  | Phòng ban hiện tại          |
| 4   | bo_phan_dich          | Many2one        | FK → phong_ban  | Phòng ban chuyển đến       |
| 5   | thoi_gian_luan_chuyen | Datetime        | Required         | Thời gian thực hiện         |
| 6   | ly_do                 | Text            | -                | Lý do luân chuyển           |
| 7   | ghi_chu               | Char            | -                | Ghi chú                       |

---

#### Bảng 3.11: thanh_ly_tai_san (Thanh lý tài sản)


| STT | Tên trường      | Kiểu dữ liệu | Ràng buộc             | Mô tả                        |
| --- | ------------------ | --------------- | ----------------------- | ------------------------------ |
| 1   | id                 | Integer         | PK, Auto                | Khóa chính, tự động tăng |
| 2   | ma_thanh_ly        | Char            | Unique, Required        | Mã phiếu thanh lý           |
| 3   | hanh_dong          | Selection       | Required                | 'ban' hoặc 'huy'              |
| 4   | tai_san_id         | Many2one        | FK → tai_san, Required | Tài sản thanh lý            |
| 5   | nguoi_thanh_ly_id  | Many2one        | FK → nhan_vien         | Người thực hiện            |
| 6   | thoi_gian_thanh_ly | Datetime        | Required                | Thời gian thanh lý           |
| 7   | ly_do_thanh_ly     | Char            | -                       | Lý do thanh lý               |
| 8   | gia_ban            | Float           | Required                | Giá bán (nếu bán)          |
| 9   | gia_goc            | Float           | Computed                | Giá gốc của tài sản       |

---

#### Bảng 3.12: lich_su_khau_hao (Lịch sử khấu hao)


| STT | Tên trường    | Kiểu dữ liệu | Ràng buộc             | Mô tả                        |
| --- | ---------------- | --------------- | ----------------------- | ------------------------------ |
| 1   | id               | Integer         | PK, Auto                | Khóa chính, tự động tăng |
| 2   | ma_ts            | Many2one        | FK → tai_san, Required | Tài sản được khấu hao    |
| 3   | ngay_khau_hao    | Date            | Required                | Ngày thực hiện khấu hao    |
| 4   | so_tien_khau_hao | Float           | Required                | Số tiền khấu hao kỳ này   |
| 5   | gia_tri_truoc    | Float           | -                       | Giá trị trước khấu hao    |
| 6   | gia_tri_sau      | Float           | -                       | Giá trị sau khấu hao        |
| 7   | phuong_phap      | Selection       | -                       | Phương pháp khấu hao       |
| 8   | ghi_chu          | Char            | -                       | Ghi chú                       |

---

#### Bảng 3.13: lich_su_ky_thuat (Lịch sử kỹ thuật)


| STT | Tên trường   | Kiểu dữ liệu | Ràng buộc             | Mô tả                        |
| --- | --------------- | --------------- | ----------------------- | ------------------------------ |
| 1   | id              | Integer         | PK, Auto                | Khóa chính, tự động tăng |
| 2   | tai_san_id      | Many2one        | FK → tai_san, Required | Tài sản liên quan           |
| 3   | ngay_ghi_nhan   | Date            | Required                | Ngày ghi nhận                |
| 4   | tinh_trang      | Selection       | Required                | Tình trạng kỹ thuật        |
| 5   | mo_ta           | Text            | -                       | Mô tả chi tiết              |
| 6   | nguoi_thuc_hien | Many2one        | FK → nhan_vien         | Người thực hiện            |

---

### 3.3.3. Chi tiết các bảng dữ liệu - Module Quản lý Tài chính

#### Bảng 3.14: phe_duyet_mua_tai_san (Phê duyệt mua tài sản)


| STT | Tên trường          | Kiểu dữ liệu | Ràng buộc               | Mô tả                                   |
| --- | ---------------------- | --------------- | ------------------------- | ----------------------------------------- |
| 1   | id                     | Integer         | PK, Auto                  | Khóa chính, tự động tăng            |
| 2   | ma_phe_duyet           | Char            | Unique, Required          | Mã phê duyệt (VD: PDMTS-00001)         |
| 3   | ngay_tao               | Date            | Required                  | Ngày tạo đơn phê duyệt              |
| 4   | de_xuat_mua_id         | Many2one        | FK → de_xuat_mua_tai_san | Đề xuất gốc từ module tài sản      |
| 5   | ma_de_xuat             | Char            | Computed                  | Mã đề xuất (lấy từ đề xuất gốc) |
| 6   | ten_de_xuat            | Char            | -                         | Tiêu đề đề xuất                     |
| 7   | ngay_de_xuat           | Date            | -                         | Ngày đề xuất gốc                     |
| 8   | nguoi_de_xuat_id       | Many2one        | FK → res.users           | Người tạo đề xuất                   |
| 9   | phong_ban_id           | Many2one        | FK → phong_ban           | Phòng ban đề xuất                     |
| 10  | tong_gia_tri           | Float           | -                         | Tổng giá trị đề xuất                |
| 11  | don_vi_tien_te         | Selection       | -                         | 'vnd' hoặc 'usd'                         |
| 12  | ly_do                  | Text            | -                         | Lý do đề xuất                         |
| 13  | mo_ta                  | Html            | -                         | Mô tả chi tiết                         |
| 14  | ngay_du_kien_nhan      | Date            | -                         | Ngày dự kiến nhận hàng               |
| 15  | state                  | Selection       | Required                  | Trạng thái phê duyệt                  |
| 16  | nguoi_phe_duyet_id     | Many2one        | FK → res.users           | Người phê duyệt                       |
| 17  | ngay_phe_duyet         | Date            | -                         | Ngày phê duyệt                         |
| 18  | ly_do_tu_choi          | Text            | -                         | Lý do từ chối (nếu có)               |
| 19  | tai_khoan_tai_san_id   | Many2one        | FK → account.account     | TK tài sản cố định (211)             |
| 20  | tai_khoan_nguon_von_id | Many2one        | FK → account.account     | TK nguồn vốn (112/1121)                 |
| 21  | so_nhat_ky_id          | Many2one        | FK → account.journal     | Sổ nhật ký ghi bút toán              |
| 22  | tai_san_ids            | Many2many       | FK → tai_san             | Danh sách tài sản đã tạo            |
| 23  | tai_san_count          | Integer         | Computed                  | Số lượng tài sản đã tạo           |

**Các giá trị State:**

- `draft`: Chờ xử lý
- `approved`: Đã phê duyệt
- `rejected`: Từ chối
- `done`: Hoàn thành
- `cancelled`: Đã hủy

---

#### Bảng 3.15: phe_duyet_mua_tai_san_line (Chi tiết phê duyệt)


| STT | Tên trường     | Kiểu dữ liệu | Ràng buộc                 | Mô tả                        |
| --- | ----------------- | --------------- | --------------------------- | ------------------------------ |
| 1   | id                | Integer         | PK, Auto                    | Khóa chính, tự động tăng |
| 2   | phe_duyet_id      | Many2one        | FK → phe_duyet_mua_tai_san | Đơn phê duyệt cha          |
| 3   | ten_thiet_bi      | Char            | Required                    | Tên thiết bị                |
| 4   | danh_muc_ts_id    | Many2one        | FK → danh_muc_tai_san      | Danh mục tài sản            |
| 5   | mo_ta             | Text            | -                           | Mô tả chi tiết              |
| 6   | thong_so_ky_thuat | Text            | -                           | Thông số kỹ thuật          |
| 7   | so_luong          | Integer         | Required                    | Số lượng                    |
| 8   | don_vi_tinh       | Char            | -                           | Đơn vị tính                |
| 9   | don_gia           | Float           | Required                    | Đơn giá                     |
| 10  | thanh_tien        | Float           | Computed                    | Thành tiền                   |
| 11  | pp_khau_hao       | Selection       | -                           | Phương pháp khấu hao       |
| 12  | thoi_gian_su_dung | Integer         | -                           | Thời gian sử dụng (năm)    |
| 13  | ty_le_khau_hao    | Float           | -                           | Tỷ lệ khấu hao (%)          |
| 14  | nha_cung_cap      | Char            | -                           | Nhà cung cấp                 |

---

#### Bảng 3.16: khau_hao_tai_san (Khấu hao tài sản)


| STT | Tên trường             | Kiểu dữ liệu | Ràng buộc                 | Mô tả                                   |
| --- | ------------------------- | --------------- | --------------------------- | ----------------------------------------- |
| 1   | id                        | Integer         | PK, Auto                    | Khóa chính, tự động tăng            |
| 2   | tai_san_id                | Many2one        | FK → tai_san, Required     | Tài sản được khấu hao               |
| 3   | phe_duyet_mua_id          | Many2one        | FK → phe_duyet_mua_tai_san | Đơn phê duyệt (nếu có)              |
| 4   | ngay_bat_dau              | Date            | Required                    | Ngày bắt đầu khấu hao                |
| 5   | gia_tri_ban_dau           | Float           | -                           | Giá trị ban đầu                       |
| 6   | thoi_gian_khau_hao        | Integer         | -                           | Thời gian khấu hao (năm)               |
| 7   | ty_le_khau_hao            | Float           | -                           | Tỷ lệ khấu hao (%/năm)                |
| 8   | phuong_phap               | Selection       | Required                    | 'straight-line', 'degressive', 'none'     |
| 9   | so_nam_khau_hao           | Integer         | Required                    | Số năm khấu hao                        |
| 10  | gia_tri_khau_hao_hang_nam | Float           | Computed                    | Giá trị khấu hao mỗi năm             |
| 11  | tong_gia_tri_khau_hao     | Float           | Computed                    | Tổng đã khấu hao                      |
| 12  | gia_tri_con_lai           | Float           | Computed                    | Giá trị còn lại                       |
| 13  | trang_thai                | Selection       | Required                    | 'dang_khau_hao', 'tam_dung', 'hoan_thanh' |

---

#### Bảng 3.17: lich_khau_hao (Lịch khấu hao chi tiết)


| STT | Tên trường    | Kiểu dữ liệu | Ràng buộc            | Mô tả                        |
| --- | ---------------- | --------------- | ---------------------- | ------------------------------ |
| 1   | id               | Integer         | PK, Auto               | Khóa chính, tự động tăng |
| 2   | khau_hao_id      | Many2one        | FK → khau_hao_tai_san | Bản ghi khấu hao cha         |
| 3   | nam              | Integer         | Required               | Năm thứ mấy                 |
| 4   | ngay_khau_hao    | Date            | Required               | Ngày khấu hao                |
| 5   | gia_tri_khau_hao | Float           | Required               | Giá trị khấu hao kỳ này   |
| 6   | da_ghi_nhan      | Boolean         | -                      | Đã ghi nhận kế toán chưa |

---

#### Bảng 3.18: but_toan (Bút toán kế toán)


| STT | Tên trường   | Kiểu dữ liệu | Ràng buộc      | Mô tả                        |
| --- | --------------- | --------------- | ---------------- | ------------------------------ |
| 1   | id              | Integer         | PK, Auto         | Khóa chính, tự động tăng |
| 2   | so_but_toan     | Char            | Unique, Required | Số bút toán (VD: BT-00001)  |
| 3   | ngay_ghi_so     | Date            | Required         | Ngày ghi sổ                  |
| 4   | dien_giai       | Char            | Required         | Diễn giải nội dung          |
| 5   | so_chung_tu_goc | Char            | -                | Số chứng từ gốc            |
| 6   | tai_khoan_no    | Char            | Required         | Tài khoản nợ                |
| 7   | tai_khoan_co    | Char            | Required         | Tài khoản có                |
| 8   | so_tien         | Float           | Required         | Số tiền                      |
| 9   | trang_thai      | Selection       | Required         | 'draft' hoặc 'posted'         |
| 10  | nguoi_tao_id    | Many2one        | FK → res.users  | Người tạo                   |
| 11  | ngay_tao        | Datetime        | Required         | Ngày tạo                     |

---

#### Bảng 3.19: tai_khoan_quan_tri (Tài khoản quản trị)


| STT | Tên trường    | Kiểu dữ liệu | Ràng buộc                 | Mô tả                        |
| --- | ---------------- | --------------- | --------------------------- | ------------------------------ |
| 1   | id               | Integer         | PK, Auto                    | Khóa chính, tự động tăng |
| 2   | ten_tai_khoan    | Char            | Required                    | Tên tài khoản               |
| 3   | ma_tai_khoan     | Char            | Required                    | Mã tài khoản                |
| 4   | phong_ban_id     | Many2one        | FK → phong_ban             | Phòng ban quản lý           |
| 5   | phe_duyet_mua_id | Many2one        | FK → phe_duyet_mua_tai_san | Phê duyệt mua liên quan     |
| 6   | ngay_ghi_nhan    | Date            | -                           | Ngày ghi nhận                |
| 7   | loai_giao_dich   | Selection       | -                           | Loại giao dịch               |
| 8   | so_tien          | Float           | -                           | Số tiền                      |
| 9   | ghi_chu          | Text            | -                           | Ghi chú                       |

---

#### Bảng 3.20: bao_cao_tai_chinh (Báo cáo tài chính)


| STT | Tên trường | Kiểu dữ liệu | Ràng buộc        | Mô tả                             |
| --- | ------------- | --------------- | ------------------ | ----------------------------------- |
| 1   | id            | Integer         | PK, Auto           | Khóa chính, tự động tăng      |
| 2   | name          | Char            | Required           | Tên báo cáo                      |
| 3   | thang         | Integer         | Required           | Tháng báo cáo                    |
| 4   | nam           | Integer         | Required           | Năm báo cáo                      |
| 5   | doanh_thu     | Float           | Computed           | Tổng doanh thu                     |
| 6   | tong_chi_phi  | Float           | Computed           | Tổng chi phí                      |
| 7   | loi_nhuan     | Float           | Computed           | Lợi nhuận = Doanh thu - Chi phí  |
| 8   | trang_thai    | Selection       | Required           | 'draft', 'in_progress', 'completed' |
| 9   | currency_id   | Many2one        | FK → res.currency | Đơn vị tiền tệ                 |
| 10  | ngay_tao      | Datetime        | Required           | Ngày tạo báo cáo                |

---

### 3.3.4. Sơ đồ quan hệ giữa các bảng

**[HÌNH 3.4: Sơ đồ quan hệ chi tiết giữa các bảng - Chèn hình ảnh tại đây]**

**Mối quan hệ chính:**

```
┌──────────────────┐     1:N     ┌──────────────────┐
│ danh_muc_tai_san │─────────────│     tai_san      │
└──────────────────┘             └──────────────────┘
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
                    ▼ 1:N                 ▼ 1:N                 ▼ 1:N
         ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
         │  phan_bo_tai_san │   │ lich_su_khau_hao │   │ thanh_ly_tai_san │
         └──────────────────┘   └──────────────────┘   └──────────────────┘

┌──────────────────────┐    1:1    ┌──────────────────────┐
│ de_xuat_mua_tai_san  │───────────│ phe_duyet_mua_tai_san│
└──────────────────────┘           └──────────────────────┘
         │ 1:N                              │ 1:N
         ▼                                  ▼
┌──────────────────────┐           ┌──────────────────────┐
│de_xuat_mua_tai_san   │           │phe_duyet_mua_tai_san │
│       .line          │           │       .line          │
└──────────────────────┘           └──────────────────────┘
```

---

## 3.4. THIẾT KẾ LUỒNG NGHIỆP VỤ

### 3.4.1. Sơ đồ luồng tổng quan hệ thống

**[HÌNH 3.5: Sơ đồ luồng tổng quan - Chèn hình ảnh tại đây]**

### 3.4.2. Luồng đề xuất và phê duyệt mua tài sản

Đây là luồng nghiệp vụ chính, thể hiện sự tích hợp giữa 2 module:

**[HÌNH 3.6: Sơ đồ luồng đề xuất mua tài sản - Chèn hình ảnh tại đây]**

**Mô tả chi tiết các bước:**


| Bước | Thực hiện bởi | Mô tả                                                   | Module      |
| ------ | ---------------- | --------------------------------------------------------- | ----------- |
| 1      | Nhân viên      | Tạo đề xuất mua tài sản (trạng thái: Draft)       | Tài sản   |
| 2      | Nhân viên      | Thêm chi tiết thiết bị, lý do, file đính kèm      | Tài sản   |
| 3      | Nhân viên      | Gửi đề xuất (trạng thái: Submitted)                 | Tài sản   |
| 4      | Hệ thống       | Tự động tạo đơn phê duyệt tại module Tài chính | Tài chính |
| 5      | Hệ thống       | Cập nhật trạng thái: Waiting_Approval                 | Tài sản   |
| 6      | Quản lý TC     | Xem xét đề xuất, cấu hình tài khoản kế toán     | Tài chính |
| 7      | Quản lý TC     | Quyết định: Phê duyệt hoặc Từ chối                | Tài chính |
| 8a     | Hệ thống       | Nếu phê duyệt: Tạo tài sản tự động               | Tài sản   |
| 8b     | Hệ thống       | Ghi bút toán kế toán (Nợ 211 / Có 112)              | Tài chính |
| 8c     | Hệ thống       | Tạo lịch khấu hao tự động                           | Tài chính |
| 9      | Hệ thống       | Cập nhật trạng thái đề xuất gốc                   | Tài sản   |
| 10     | Hệ thống       | Thông báo kết quả cho người đề xuất              | Cả 2       |

---

### 3.4.3. Luồng quản lý vòng đời tài sản

**[HÌNH 3.7: Sơ đồ vòng đời tài sản - Chèn hình ảnh tại đây]**

**Các trạng thái tài sản:**


| Trạng thái    | Mô tả                                | Chuyển tiếp được phép                      |
| --------------- | -------------------------------------- | ------------------------------------------------ |
| Chưa phân bổ | Tài sản mới tạo, chưa gán cho ai | → Đã phân bổ, → Đã thanh lý             |
| Đã phân bổ  | Đã gán cho phòng ban/nhân viên   | → Chưa phân bổ (thu hồi), → Đã thanh lý |
| Đang sử dụng | Nhân viên đang sử dụng            | → Đã phân bổ, → Bảo dưỡng               |
| Bảo dưỡng    | Đang sửa chữa/bảo trì             | → Đang sử dụng                               |
| Đã thanh lý  | Đã bán hoặc tiêu hủy             | (Trạng thái cuối)                             |

---

### 3.4.4. Luồng mượn/trả tài sản

**[HÌNH 3.8: Sơ đồ luồng mượn trả tài sản - Chèn hình ảnh tại đây]**

**Mô tả quy trình:**


| Bước | Actor       | Hành động                          | Trạng thái           |
| ------ | ----------- | ------------------------------------- | ---------------------- |
| 1      | Nhân viên | Tạo đơn mượn tài sản           | Đang chờ             |
| 2      | Quản lý   | Xem xét và duyệt/từ chối         | Đã duyệt/Từ chối  |
| 3      | Hệ thống  | Tạo phiếu mượn/trả (nếu duyệt) | Đang mượn           |
| 4      | Hệ thống  | Theo dõi thời hạn                  | Đang mượn/Quá hạn |
| 5      | Nhân viên | Trả tài sản                        | Đã trả              |

---

### 3.4.5. Luồng kiểm kê tài sản

**[HÌNH 3.9: Sơ đồ luồng kiểm kê - Chèn hình ảnh tại đây]**

**Quy trình kiểm kê:**


| Bước | Mô tả                                                                 |
| ------ | ----------------------------------------------------------------------- |
| 1      | Tạo phiếu kiểm kê, chọn phòng ban                                 |
| 2      | Hệ thống tự động load danh sách tài sản của phòng ban         |
| 3      | Kiểm kê từng tài sản, ghi nhận kết quả (Tồn tại/Thiếu/Hỏng) |
| 4      | Cập nhật tình trạng tài sản nếu cần                             |
| 5      | Hoàn thành phiếu kiểm kê, tạo báo cáo                           |

---

### 3.4.6. Luồng khấu hao tài sản

**[HÌNH 3.10: Sơ đồ luồng khấu hao - Chèn hình ảnh tại đây]**

**Phương pháp khấu hao được hỗ trợ:**


| Phương pháp       | Công thức                                 | Ví dụ                     |
| -------------------- | ------------------------------------------- | --------------------------- |
| **Tuyến tính**     | Khấu hao = Giá trị ban đầu / Số năm  | 100tr / 5 năm = 20tr/năm  |
| **Giảm dần**       | Khấu hao = Giá trị còn lại × Tỷ lệ% | Năm 1: 100tr × 20% = 20tr |
| **Không khấu hao** | Không tạo lịch khấu hao                 | -                           |

**Bút toán khấu hao:**

- **Nợ**: TK 642 - Chi phí khấu hao
- **Có**: TK 214 - Khấu hao lũy kế TSCĐ

---

### 3.4.7. Luồng thanh lý tài sản

**[HÌNH 3.11: Sơ đồ luồng thanh lý - Chèn hình ảnh tại đây]**

**Các hành động thanh lý:**


| Hành động   | Mô tả                                    | Yêu cầu        |
| -------------- | ------------------------------------------ | ---------------- |
| **Bán**       | Bán tài sản cho bên thứ ba            | Giá bán > 0    |
| **Tiêu hủy** | Tiêu hủy tài sản không còn giá trị | Ghi nhận lý do |

**Quy tắc nghiệp vụ:**

- Mỗi tài sản chỉ thanh lý được một lần
- Thu hồi phân bổ trước khi thanh lý
- Tự động cập nhật trạng thái tài sản = "Đã thanh lý"

---

## 3.5. THIẾT KẾ GIAO DIỆN NGƯỜI DÙNG

### 3.5.1. Cấu trúc menu hệ thống

#### A. Menu Module Quản lý Tài sản

```
📁 Quản lý tài sản
├── 📊 Dashboard
│   ├── Tổng quan
│   └── Danh sách mượn trả
├── 🏷️ Tài sản
│   ├── Loại tài sản
│   ├── Quản lý tài sản cụ thể
│   └── Phân bổ tài sản
├── 📈 Khấu hao/Kiểm kê
│   ├── Khấu hao tài sản
│   └── Kiểm kê tài sản
├── 🔄 Luân chuyển/Thanh lý
│   ├── Quản lý luân chuyển tài sản
│   └── Thanh lý tài sản
├── 📋 Mượn trả tài sản
│   ├── Đơn mượn tài sản
│   └── Quản lý mượn trả tài sản
└── 📝 Đề xuất mua tài sản
```

#### B. Menu Module Quản lý Tài chính

```
📁 Quản lý tài chính
├── 📊 Dashboard
├── ✅ Phê duyệt mua tài sản
├── 📉 Khấu hao
│   ├── Khấu hao tài sản
│   └── Tính khấu hao tự động
├── 💰 Kế toán
│   ├── Bút toán
│   └── Tài khoản quản trị
└── 📊 Báo cáo tài chính
```

### 3.5.2. Thiết kế các màn hình chính

#### A. Dashboard Tổng quan Tài sản

**[HÌNH 3.12: Giao diện Dashboard Tổng quan Tài sản - Chèn hình ảnh tại đây]**

**Các thành phần:**

- **KPI Cards**: Tổng tài sản, Đang sử dụng, Không sử dụng, Đã thanh lý
- **Biểu đồ tròn**: Phân bổ theo loại tài sản
- **Biểu đồ cột**: Phân bổ theo phòng ban
- **Bảng Top**: Tài sản giá trị cao nhất

---

#### B. Form Tài sản

**[HÌNH 3.13: Giao diện Form Tài sản - Chèn hình ảnh tại đây]**

**Layout:**

- **Header**: Mã tài sản, Tên tài sản, Trạng thái
- **Tab Thông tin chung**: Thông tin cơ bản, giá trị, danh mục
- **Tab Khấu hao**: Phương pháp, thời gian, tỷ lệ
- **Tab Phân bổ**: Lịch sử phân bổ cho phòng ban
- **Tab Lịch sử**: Khấu hao, kiểm kê, luân chuyển

---

#### C. Form Đề xuất mua tài sản

**[HÌNH 3.14: Giao diện Form Đề xuất mua - Chèn hình ảnh tại đây]**

**Layout:**

- **Header**: Mã đề xuất, Trạng thái, Buttons (Gửi/Hủy)
- **Thông tin đề xuất**: Tiêu đề, Người đề xuất, Phòng ban, Ngày
- **Chi tiết thiết bị**: Table với các dòng thiết bị
- **Tổng giá trị**: Tự động tính từ chi tiết
- **Lý do & Mô tả**: Rich text editor
- **File đính kèm**: Upload multiple files

---

#### D. Dashboard Tài chính

**[HÌNH 3.15: Giao diện Dashboard Tài chính - Chèn hình ảnh tại đây]**

**Các thành phần:**

- **Section Phê duyệt**: Tổng đơn, Chờ duyệt, Đã duyệt, Từ chối
- **Section Khấu hao**: Tổng tài sản, Đang khấu hao, Giá trị còn lại
- **Section Bút toán**: Tổng bút toán, Nháp, Đã ghi sổ
- **Biểu đồ**: Trend khấu hao, Phân bổ chi phí

---

#### E. Form Phê duyệt mua tài sản

**[HÌNH 3.16: Giao diện Form Phê duyệt - Chèn hình ảnh tại đây]**

**Layout:**

- **Header**: Mã phê duyệt, Trạng thái, Buttons (Phê duyệt/Từ chối)
- **Thông tin đề xuất**: Readonly từ đề xuất gốc
- **Chi tiết thiết bị**: Table readonly
- **Cấu hình tài khoản**: TK Tài sản, TK Nguồn vốn, Sổ nhật ký
- **Tài sản đã tạo**: Smart button link đến danh sách tài sản

---

### 3.5.3. Thiết kế báo cáo

#### A. Báo cáo Tài chính

**[HÌNH 3.17: Mẫu báo cáo tài chính - Chèn hình ảnh tại đây]**

**Nội dung báo cáo:**

- **Header**: Tên công ty, Tiêu đề báo cáo, Kỳ báo cáo
- **KPI Summary**: Doanh thu, Chi phí, Lợi nhuận
- **Chi tiết**: Bảng breakdown theo danh mục
- **Footer**: Người lập, Ngày lập, Chữ ký

---

## 3.6. TRIỂN KHAI HỆ THỐNG

### 3.6.1. Môi trường triển khai


| Thành phần     | Công nghệ/Phiên bản           |
| ---------------- | --------------------------------- |
| Hệ điều hành | Ubuntu 20.04 LTS / Windows Server |
| Database         | PostgreSQL 12+                    |
| Web Server       | Nginx (reverse proxy)             |
| Application      | Odoo 15 Community                 |
| Python           | Python 3.8+                       |

### 3.6.2. Cấu trúc thư mục module

```
quan_ly_tai_san/
├── __init__.py
├── __manifest__.py
├── controllers/
│   └── controllers.py
├── data/
│   ├── sequence.xml
│   └── tai_san_demo.xml
├── models/
│   ├── __init__.py
│   ├── danh_muc_tai_san.py
│   ├── tai_san.py
│   ├── phan_bo_tai_san.py
│   ├── de_xuat_mua_tai_san.py
│   ├── don_muon_tai_san.py
│   ├── muon_tra_tai_san.py
│   ├── kiem_ke_tai_san.py
│   ├── luan_chuyen_tai_san.py
│   ├── thanh_ly_tai_san.py
│   ├── lich_su_khau_hao.py
│   ├── lich_su_ky_thuat.py
│   └── dashboard.py
├── security/
│   └── ir.model.access.csv
├── static/
│   ├── css/
│   ├── js/
│   └── description/
│       └── icon.png
└── views/
    ├── danh_muc_tai_san.xml
    ├── tai_san.xml
    ├── phan_bo_tai_san.xml
    ├── de_xuat_mua_tai_san_views.xml
    ├── don_muon_tai_san.xml
    ├── muon_tra_tai_san.xml
    ├── kiem_ke_tai_san.xml
    ├── luan_chuyen_tai_san.xml
    ├── thanh_ly_tai_san.xml
    ├── lich_su_khau_hao.xml
    ├── dashboard_overview.xml
    ├── dashboard_borrowing.xml
    └── menu.xml
```

```
quan_ly_tai_chinh/
├── __init__.py
├── __manifest__.py
├── controllers/
│   └── controllers.py
├── data/
│   ├── sequence.xml
│   └── tai_chinh_demo.xml
├── models/
│   ├── __init__.py
│   ├── phe_duyet_mua_tai_san.py
│   ├── khau_hao_tai_san.py
│   ├── but_toan.py
│   ├── tai_khoan_quan_tri.py
│   ├── bao_cao_tai_chinh.py
│   ├── dashboard_tai_chinh.py
│   ├── tinh_toan_khau_hao.py
│   └── wizard_sao_chep.py
├── report/
│   └── bao_cao_tai_chinh_report.xml
├── security/
│   └── ir.model.access.csv
├── static/
│   ├── css/
│   │   ├── dashboard_style.css
│   │   └── bao_cao_style.css
│   ├── js/
│   │   ├── dashboard_tai_chinh.js
│   │   └── bao_cao_charts.js
│   └── description/
│       └── icon.png
└── views/
    ├── phe_duyet_mua_tai_san_views.xml
    ├── khau_hao_tai_san_views.xml
    ├── but_toan_views.xml
    ├── tai_khoan_quan_tri_views.xml
    ├── bao_cao_tai_chinh_views.xml
    ├── dashboard_tai_chinh_views.xml
    ├── tinh_toan_khau_hao_views.xml
    ├── wizard_sao_chep_views.xml
    └── menu.xml
```

### 3.6.3. Hướng dẫn cài đặt

**Bước 1**: Clone source code vào thư mục addons của Odoo

```bash
cd /path/to/odoo/addons
git clone <repository_url>
```

**Bước 2**: Cập nhật danh sách module

```bash
./odoo-bin -c odoo.conf -u all -d <database_name>
```

**Bước 3**: Cài đặt module qua giao diện

- Truy cập: Apps → Cập nhật danh sách ứng dụng
- Tìm kiếm: "quan_ly_tai_san" hoặc "quan_ly_tai_chinh"
- Click "Cài đặt"

**Lưu ý**: Cài đặt module `quan_ly_tai_san` trước, sau đó mới cài `quan_ly_tai_chinh` do có phụ thuộc.

---

## 3.7. TÍCH HỢP 2 MODULE

### 3.7.1. Điểm tích hợp chính

**[HÌNH 3.18: Sơ đồ tích hợp 2 module - Chèn hình ảnh tại đây]**


| Điểm tích hợp            | Module nguồn | Module đích | Mô tả                                               |
| ---------------------------- | ------------- | ------------- | ----------------------------------------------------- |
| 1. Đề xuất → Phê duyệt | Tài sản     | Tài chính   | Tự động tạo đơn phê duyệt khi gửi đề xuất |
| 2. Phê duyệt → Tài sản  | Tài chính   | Tài sản     | Tự động tạo tài sản khi phê duyệt             |
| 3. Phê duyệt → Khấu hao  | Tài chính   | Tài chính   | Tự động tạo lịch khấu hao                       |
| 4. Đồng bộ trạng thái   | Tài chính   | Tài sản     | Cập nhật trạng thái đề xuất gốc               |

### 3.7.2. Luồng tích hợp chi tiết

**[HÌNH 3.19: Sequence Diagram tích hợp - Chèn hình ảnh tại đây]**

```
Sequence Diagram - Luồng tích hợp mua tài sản:

Nhân viên → Module Tài sản: 1. Tạo đề xuất mua
Module Tài sản → Module Tài sản: 2. Validate & Save
Nhân viên → Module Tài sản: 3. Gửi đề xuất
Module Tài sản → Module Tài chính: 4. Tạo đơn phê duyệt
Module Tài chính → Module Tài chính: 5. Lưu đơn phê duyệt

[Quản lý tài chính xem xét]

Module Tài chính → Module Tài chính: 6. Phê duyệt
Module Tài chính → Module Tài sản: 7. Tạo tài sản
Module Tài chính → Sổ cái: 8. Ghi bút toán
Module Tài chính → Module Tài chính: 9. Tạo lịch khấu hao
Module Tài chính → Module Tài sản: 10. Cập nhật trạng thái
Module Tài sản → Nhân viên: 11. Thông báo kết quả
```

### 3.7.3. Điểm mạnh của việc tích hợp 2 module

#### A. Lợi ích về quy trình


| STT | Lợi ích                  | Mô tả                                                                 |
| --- | -------------------------- | ----------------------------------------------------------------------- |
| 1   | **Tự động hóa cao**    | Tạo tài sản, ghi sổ, khấu hao tự động khi phê duyệt           |
| 2   | **Kiểm soát chặt chẽ** | Phân tách quyền: Đề xuất (Tài sản) ≠ Phê duyệt (Tài chính) |
| 3   | **Đồng bộ realtime**    | Trạng thái cập nhật tức thời giữa 2 module                       |
| 4   | **Truy vết đầy đủ**   | Theo dõi từ đề xuất → phê duyệt → tài sản → khấu hao       |
| 5   | **Giảm sai sót**         | Loại bỏ nhập liệu thủ công trùng lặp                            |

#### B. Lợi ích về quản lý


| STT | Lợi ích                  | Mô tả                                                     |
| --- | -------------------------- | ----------------------------------------------------------- |
| 1   | **Dashboard tích hợp**   | Xem tổng quan cả tài sản và tài chính tại một nơi |
| 2   | **Báo cáo liên module** | Báo cáo ROI, hiệu quả sử dụng tài sản               |
| 3   | **Quản lý ngân sách**  | Kiểm soát chi tiêu mua sắm theo phòng ban              |
| 4   | **Dự báo khấu hao**     | Lập kế hoạch chi phí khấu hao tương lai              |

#### C. Lợi ích về kỹ thuật


| STT | Lợi ích                  | Mô tả                                                |
| --- | -------------------------- | ------------------------------------------------------ |
| 1   | **Modular design**         | Có thể sử dụng riêng từng module hoặc kết hợp |
| 2   | **Mở rộng dễ dàng**    | Thêm tính năng mới mà không ảnh hưởng core    |
| 3   | **Bảo trì thuận tiện** | Sửa lỗi, nâng cấp theo module độc lập           |
| 4   | **Tái sử dụng code**    | Các utility function dùng chung                      |

### 3.7.4. Xử lý lỗi và recovery


| Tình huống lỗi             | Xử lý                              | Recovery                      |
| ----------------------------- | ------------------------------------ | ----------------------------- |
| Lỗi tạo tài sản           | Rollback toàn bộ, thông báo user | User sửa dữ liệu và retry |
| Lỗi ghi sổ kế toán        | Log warning, tài sản vẫn tạo     | Admin ghi sổ thủ công      |
| Lỗi tạo khấu hao           | Log warning, tài sản vẫn tạo     | Setup khấu hao thủ công    |
| Module tài chính chưa cài | Block gửi đề xuất                | Yêu cầu cài module         |

---

## 3.8. ĐÁNH GIÁ VÀ KẾT LUẬN

### 3.8.1. Tổng kết các chức năng đã triển khai

**Module Quản lý Tài sản (quan_ly_tai_san):**

- ✅ 9 nhóm chức năng chính
- ✅ 13 bảng dữ liệu
- ✅ Dashboard trực quan
- ✅ Workflow đầy đủ các trạng thái

**Module Quản lý Tài chính (quan_ly_tai_chinh):**

- ✅ 6 nhóm chức năng chính
- ✅ 7 bảng dữ liệu
- ✅ Dashboard tài chính
- ✅ Báo cáo tài chính

**Tích hợp 2 module:**

- ✅ 4 điểm tích hợp chính
- ✅ Tự động hóa quy trình mua sắm
- ✅ Đồng bộ dữ liệu realtime
- ✅ Xử lý lỗi và recovery

### 3.8.2. Ưu điểm của hệ thống


| Tiêu chí            | Đánh giá                                          |
| --------------------- | ---------------------------------------------------- |
| **Tính toàn diện** | Quản lý toàn bộ vòng đời tài sản            |
| **Tích hợp**        | Kết nối chặt chẽ giữa tài sản và tài chính |
| **Tự động hóa**   | Giảm thiểu thao tác thủ công                    |
| **Truy vết**         | Lịch sử đầy đủ cho audit                       |
| **Mở rộng**         | Dễ dàng thêm tính năng mới                     |
| **Giao diện**        | Thân thiện, dễ sử dụng                          |

### 3.8.3. Hướng phát triển tương lai


| STT | Tính năng     | Mô tả                                         |
| --- | --------------- | ----------------------------------------------- |
| 1   | Mobile App      | Ứng dụng di động cho kiểm kê, mượn trả |
| 2   | QR/Barcode      | Quét mã để tra cứu tài sản nhanh         |
| 3   | AI/ML           | Dự báo nhu cầu mua sắm, bảo trì           |
| 4   | IoT Integration | Theo dõi vị trí tài sản realtime           |
| 5   | API Gateway     | Tích hợp với hệ thống ERP khác            |
| 6   | Blockchain      | Đảm bảo tính bất biến lịch sử tài sản |

---

## PHỤ LỤC

### Phụ lục A: Danh sách các trường computed


| Model                    | Trường                  | Công thức                                         |
| ------------------------ | ------------------------- | --------------------------------------------------- |
| tai_san                  | trang_thai_thanh_ly       | Computed từ thanh_ly_ids và phong_ban_su_dung_ids |
| de_xuat_mua_tai_san      | tong_gia_tri              | SUM(line_ids.thanh_tien)                            |
| de_xuat_mua_tai_san.line | thanh_tien                | so_luong × don_gia                                 |
| khau_hao_tai_san         | gia_tri_khau_hao_hang_nam | gia_tri_ban_dau / so_nam_khau_hao                   |
| khau_hao_tai_san         | tong_gia_tri_khau_hao     | gia_tri_khau_hao_hang_nam × so_nam_khau_hao        |
| khau_hao_tai_san         | gia_tri_con_lai           | gia_tri_ban_dau - tong_gia_tri_khau_hao             |
| muon_tra_tai_san         | tinh_trang                | Computed từ trang_thai và thoi_gian               |
| kiem_ke_tai_san          | trang_thai_phieu          | Computed từ ds_kiem_ke_ids.trang_thai              |

### Phụ lục B: Danh sách các workflow states


| Model                 | States                                                                |
| --------------------- | --------------------------------------------------------------------- |
| de_xuat_mua_tai_san   | draft → submitted → waiting_approval → approved/rejected/cancelled |
| phe_duyet_mua_tai_san | draft → approved/rejected → done/cancelled                          |
| don_muon_tai_san      | dang-cho → da-duyet/tu-choi                                          |
| muon_tra_tai_san      | dang-muon → da-tra                                                   |
| kiem_ke_tai_san_line  | in-progress → finished                                               |
| but_toan              | draft → posted                                                       |
| khau_hao_tai_san      | dang_khau_hao → tam_dung/hoan_thanh                                  |

### Phụ lục C: Danh sách các ràng buộc (Constraints)


| Model            | Constraint                   | Mô tả                                 |
| ---------------- | ---------------------------- | --------------------------------------- |
| danh_muc_tai_san | ma_danh_muc_ts_unique        | Mã loại tài sản phải duy nhất     |
| tai_san          | ma_tai_san_unique            | Mã tài sản phải duy nhất           |
| tai_san          | _check_gia_tri               | Giá trị hiện tại không được âm |
| don_muon_tai_san | ma_don_muon_unique           | Mã đơn mượn phải duy nhất        |
| muon_tra_tai_san | _constrains_thoi_gian        | Thời gian mượn < Thời gian trả     |
| thanh_ly_tai_san | ma_thanh_ly_unique           | Mã thanh lý phải duy nhất           |
| thanh_ly_tai_san | _constrains_gia_ban          | Giá bán >= 0                          |
| thanh_ly_tai_san | _check_tai_san_thanh_ly_once | Một tài sản chỉ thanh lý một lần |

---

**Kết thúc Chương 3**
