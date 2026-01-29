# Tài liệu API - Kết nối Ứng dụng Ngoài

## 1. Giới thiệu

Hệ thống Quản lý Tài sản & Tài chính được xây dựng trên nền tảng Odoo 15, cung cấp khả năng tích hợp với các ứng dụng bên ngoài thông qua giao thức **JSON-RPC** (JavaScript Object Notation - Remote Procedure Call).

### 1.1 Mục đích
- Cho phép ứng dụng di động, web app hoặc hệ thống bên thứ ba truy cập dữ liệu
- Thực hiện các thao tác CRUD (Create, Read, Update, Delete) từ xa
- Xác thực người dùng qua API

### 1.2 Giao thức sử dụng
| Giao thức | Mô tả |
|-----------|-------|
| **JSON-RPC 2.0** | Giao thức RPC sử dụng JSON để mã hóa dữ liệu |
| **HTTP/HTTPS** | Giao thức truyền tải |
| **REST-like** | Có thể đóng gói thành REST API qua middleware |

---

## 2. Kiến trúc Tích hợp

```
┌─────────────────────┐       ┌─────────────────────┐       ┌─────────────────────┐
│   Ứng dụng Ngoài    │       │   Middleware        │       │   Odoo Server       │
│   (Mobile/Web)      │──────▶│   (Node.js/Python)  │──────▶│   (JSON-RPC)        │
│                     │ REST  │                     │ RPC   │                     │
└─────────────────────┘       └─────────────────────┘       └─────────────────────┘
```

### 2.1 Các thành phần
| Thành phần | Vai trò |
|------------|---------|
| **Ứng dụng Client** | Gửi request, nhận response, hiển thị dữ liệu |
| **Middleware (tùy chọn)** | Chuyển đổi REST sang JSON-RPC, xử lý authentication |
| **Odoo Server** | Xử lý business logic, truy vấn database |

---

## 3. Cơ chế Xác thực

### 3.1 Quy trình xác thực
1. Client gửi thông tin đăng nhập (database, username, password)
2. Server xác thực và trả về **User ID (UID)**
3. Client sử dụng UID cho các request tiếp theo

### 3.2 Thông tin xác thực cần thiết
| Tham số | Mô tả |
|---------|-------|
| **Database** | Tên cơ sở dữ liệu Odoo |
| **Username** | Tên đăng nhập người dùng |
| **Password** | Mật khẩu người dùng |
| **UID** | ID người dùng (nhận được sau khi đăng nhập) |

### 3.3 Bảo mật
- Mật khẩu được truyền qua HTTPS để mã hóa
- UID được sử dụng để xác thực các request tiếp theo
- Hỗ trợ cơ chế session hoặc token-based authentication

---

## 4. Các Endpoint API

### 4.1 Endpoint chính
| Endpoint | Mô tả |
|----------|-------|
| `/jsonrpc` | Endpoint JSON-RPC chính |
| `/xmlrpc/2/common` | Xác thực (XML-RPC) |
| `/xmlrpc/2/object` | Thực thi method (XML-RPC) |

### 4.2 Service Types
| Service | Mô tả |
|---------|-------|
| **common** | Xác thực, kiểm tra version |
| **object** | Thực thi các method trên model |
| **db** | Quản lý database |

---

## 5. Các Phương thức API

### 5.1 Phương thức Đọc dữ liệu

| Phương thức | Mô tả | Tham số |
|-------------|-------|---------|
| **search** | Tìm kiếm ID theo điều kiện | domain (điều kiện lọc) |
| **read** | Đọc dữ liệu theo ID | ids, fields |
| **search_read** | Tìm kiếm và đọc dữ liệu | domain, fields, limit, offset |
| **search_count** | Đếm số bản ghi | domain |

### 5.2 Phương thức Ghi dữ liệu

| Phương thức | Mô tả | Tham số |
|-------------|-------|---------|
| **create** | Tạo bản ghi mới | values (dict) |
| **write** | Cập nhật bản ghi | ids, values |
| **unlink** | Xóa bản ghi | ids |

### 5.3 Phương thức Đặc biệt

| Phương thức | Mô tả |
|-------------|-------|
| **name_get** | Lấy tên hiển thị của bản ghi |
| **name_search** | Tìm kiếm theo tên |
| **fields_get** | Lấy thông tin các field của model |
| **default_get** | Lấy giá trị mặc định |

---

## 6. Domain Filter (Điều kiện Lọc)

### 6.1 Cấu trúc Domain
Domain là danh sách các tuple với cấu trúc: `(field, operator, value)`

### 6.2 Các Operator

| Operator | Mô tả | Ví dụ |
|----------|-------|-------|
| `=` | Bằng | `('state', '=', 'active')` |
| `!=` | Khác | `('state', '!=', 'draft')` |
| `>`, `<`, `>=`, `<=` | So sánh | `('amount', '>', 1000)` |
| `like` | Chứa (có phân biệt hoa thường) | `('name', 'like', 'ABC')` |
| `ilike` | Chứa (không phân biệt) | `('name', 'ilike', 'abc')` |
| `in` | Trong danh sách | `('id', 'in', [1,2,3])` |
| `not in` | Không trong danh sách | `('id', 'not in', [1,2])` |

### 6.3 Toán tử Logic

| Toán tử | Mô tả |
|---------|-------|
| `&` | AND (mặc định) |
| `|` | OR |
| `!` | NOT |

---

## 7. Danh sách Model và API

### 7.1 Module Nhân sự

| Model | Mô tả | API Method đặc biệt |
|-------|-------|---------------------|
| `nhan_vien` | Nhân viên | `web_login`, `web_register`, `get_employee_by_username` |
| `phong_ban` | Phòng ban | CRUD chuẩn |
| `chuc_vu` | Chức vụ | CRUD chuẩn |

### 7.2 Module Quản lý Tài sản

| Model | Mô tả | API Method đặc biệt |
|-------|-------|---------------------|
| `tai_san` | Tài sản | CRUD chuẩn |
| `danh_muc_tai_san` | Danh mục | CRUD chuẩn |
| `phan_bo_tai_san` | Phân bổ | CRUD chuẩn |
| `don_muon_tai_san` | Đơn mượn | `action_duyet`, `action_tra` |
| `thanh_ly_tai_san` | Thanh lý | CRUD chuẩn |

### 7.3 Module Quản lý Tài chính

| Model | Mô tả | API Method đặc biệt |
|-------|-------|---------------------|
| `khau_hao_tai_san` | Khấu hao | `tinh_khau_hao` |
| `phe_duyet_mua_tai_san` | Phê duyệt | `action_approve`, `action_reject` |
| `but_toan` | Bút toán | CRUD chuẩn |
| `bao_cao_tai_chinh` | Báo cáo | `generate_report` |

---

## 8. Xử lý Lỗi

### 8.1 Mã lỗi HTTP

| Mã | Mô tả |
|----|-------|
| 200 | Thành công |
| 400 | Request không hợp lệ |
| 401 | Chưa xác thực |
| 403 | Không có quyền |
| 404 | Không tìm thấy |
| 500 | Lỗi server |

### 8.2 Cấu trúc Response Lỗi

Response lỗi chứa thông tin:
- **code**: Mã lỗi
- **message**: Thông báo lỗi
- **data**: Chi tiết lỗi (debug mode)

---

## 9. Best Practices

### 9.1 Hiệu suất
- Sử dụng `fields` parameter để chỉ lấy các trường cần thiết
- Sử dụng `limit` và `offset` cho phân trang
- Cache UID sau khi đăng nhập

### 9.2 Bảo mật
- Luôn sử dụng HTTPS trong production
- Không lưu password ở client
- Sử dụng token với thời hạn ngắn

### 9.3 Xử lý lỗi
- Luôn kiểm tra response error
- Implement retry logic cho network errors
- Log lỗi để debug

---

## 10. Tóm tắt

| Thành phần | Công nghệ |
|------------|-----------|
| Giao thức | JSON-RPC 2.0 |
| Xác thực | Username/Password → UID |
| Endpoint | `/jsonrpc` |
| Định dạng | JSON |
| Bảo mật | HTTPS, Token-based |

| Thống kê | Số lượng |
|----------|----------|
| Tổng Model | 15+ |
| Phương thức CRUD | 6 |
| API đặc biệt | 10+ |
