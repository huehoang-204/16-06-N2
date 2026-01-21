---
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![GitLab](https://img.shields.io/badge/gitlab-%23181717.svg?style=for-the-badge&logo=gitlab&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)


# 1. Giới thiệu về dự án

## 1.1. Tổng quan
Hệ thống quản lý tài sản và tài chính tích hợp được thiết kế để tối ưu hóa quy trình kiểm soát, theo dõi và quản lý tài sản cố định cũng như các hoạt động tài chính liên quan trong tổ chức. Giải pháp này kết hợp hai module chính:
- **Quản lý Tài sản**: Theo dõi vòng đời tài sản từ mua sắm đến thanh lý
- **Quản lý Tài chính**: Xử lý khía cạnh kế toán, khấu hao và kiểm soát chi tiêu

---

## 1.2. Các chức năng chính

### **Module Quản lý Tài sản**

#### 1. Dashboard tổng quan và tình hình mượn trả
Cung cấp cái nhìn 360° về tình trạng tài sản của tổ chức:
- Số lượng tài sản hiện có trong hệ thống
- Số lượng tài sản đang bị lỗi/hư hỏng
- Dự báo nhu cầu mua sắm trong tương lai

#### 2. Quản lý loại tài sản
Chuẩn hóa phân loại tài sản trong toàn tổ chức:
- Tối ưu hóa quy trình kế toán - không cần định khoản lại cho mỗi lần mua mới
- Tự động áp dụng chính sách khấu hao tiêu chuẩn (vd: Laptop → khấu hao 3 năm → TK 211)
- Đảm bảo nhất quán dữ liệu và báo cáo

#### 3. Quản lý tài sản cụ thể
Xây dựng "hồ sơ lý lịch" chi tiết cho từng tài sản (Digital Twin):
- Theo dõi Serial Number, Model, nhà cung cấp
- Lưu trữ lịch sử bảo trì, sửa chữa
- Ghi nhận giá trị khấu hao và tuổi thọ
- Tạo QR Code cho quản lý hàng tồn kho

#### 4. Phân bổ tài sản cho các phòng ban
Xác định rõ ràng trách nhiệm vật lý và tài chính:
- Tài sản nằm ở phòng nào → phòng đó chịu trách nhiệm bảo quản
- Phân bổ chi phí khấu hao theo đơn vị sử dụng
- Thuận lợi cho báo cáo chi phí theo bộ phận

#### 5. Kiểm kê tài sản
Đối chiếu định kỳ giữa "Phần mềm" (hệ thống) và "Thực tế" (kho):
- Phát hiện tài sản mất mát, hư hỏng hoặc thất thoát
- Điều chỉnh sổ sách khi có chênh lệch
- Đảm bảo độ chính xác của dữ liệu tài chính

#### 6. Luân chuyển tài sản
Linh hoạt trong quản lý nhân sự và cơ cấu tổ chức:
- Chuyển tài sản giữa nhân viên khi có thay đổi nhân sự
- Chuyển tài sản giữa các chi nhánh/phòng ban
- Duy trì lịch sử luân chuyển để kiểm toán

#### 7. Thanh lý tài sản
Xử lý tài sản hết giá trị sử dụng:
- Ghi nhận tài sản hư hỏng không thể sửa chữa
- Thu hồi vốn nếu bán được
- Làm sạch sổ sách kế toán

#### 8. Quản lý đơn mượn tài sản & cấp phát tài sản
Quy trình hóa việc yêu cầu/cấp phát thiết bị:
- Tránh cấp phát tùy tiện, không có kiểm soát
- Theo dõi tài sản được mượn/cấp và thời hạn trả
- Đảm bảo tuân thủ ngân sách và chính sách

#### 9. Đơn đề xuất mua tài sản & Duyệt đơn mượn **(NEW)**
Kiểm soát và phê duyệt các yêu cầu:
- Tạo và theo dõi đơn đề xuất mua sắm tài sản
- Workflow phê duyệt rõ ràng từ lập đơn → duyệt → thực hiện mua
- Duyệt/từ chối yêu cầu mượn tài sản theo quy định

---

### **Module Quản lý Tài chính**

#### 1. Dashboard tài chính
Giao diện tổng hợp với thiết kế card-based hiện đại:
- **Thống kê phê duyệt**: Tổng, chờ duyệt, đã duyệt, hoàn thành, từ chối
- **Thống kê khấu hao**: Tổng tài sản, đang khấu hao, giá trị còn lại
- **Thống kê bút toán**: Tổng, đã ghi nhận, nhập, giá trị toàn bộ
- **Thống kê kế toán quản trị**: Tổng chi phí, chi phí tháng hiện tại
- **Biểu đồ dữ liệu**: 4 loại biểu đồ trực quan (Doughnut, Pie, Line, Bar)
- Nút action nhanh để điều hướng đến danh sách liên quan

#### 2. Khấu hao tài sản
Phân bổ chi phí mua tài sản vào nhiều kỳ kế toán:
- Tuân thủ nguyên tắc "Phù hợp" của kế toán
- Tính toán khấu hao theo phương pháp đường thẳng
- Tự động sinh bút toán khấu hao hàng kỳ

#### 3. Bút toán khấu hao
Hành động pháp lý để ghi nhận chi phí vào Sổ cái:
- Không có bút toán → báo cáo tài chính sai
- Tự động tạo bút toán khấu hao từ lịch khấu hao
- Kiểm soát các bút toán theo trạng thái (Nháp, Đã ghi nhận)

#### 4. Đơn đề xuất mua tài sản
Kiểm soát chi tiêu đầu vào (CAPEX):
- Tạo đơn đề xuất mua với bOMM chi tiết
- Duyệt theo quy trình phê duyệt có thẩm quyền
- Ngăn chặn mua sắm vượt ngân sách

#### 5. Tài khoản quản trị
Phân bổ chi phí theo bộ phận:
- Ghi nhận chi phí vận hành từng phòng ban
- Phân tích "Chi phí này của bộ phận nào?"
- Hỗ trợ báo cáo chi phí theo đơn vị

#### 6. Báo cáo tài chính
Tạo các báo cáo tuân thủ tiêu chuẩn kế toán:
- Bảng cân đối kế toán
- Báo cáo kết quả kinh doanh
- Báo cáo dòng tiền
- Chi tiết khấu hao và giá trị tài sản

#### 7. Dự báo ngân sách mua sắm **(NEW)**
Lập kế hoạch tài chính dài hạn:
- Dự báo nhu cầu thay thế tài sản cũ trong năm
- Tính toán ngân sách CAPEX dựa trên lịch khấu hao
- Tích hợp lịch sử mượn/trả để xác định tài sản cần thanh lý
- Xác định tài sản nào thanh lý được giá tốt nhất

#### 8. Quản lý đơn mua tài sản
Theo dõi toàn bộ quy trình mua sắm:
- Từ đơn đề xuất → phê duyệt → hợp đồng → nhận hàng → thanh toán
- Liên kết với kế toán cho phép ghi nhận tài sản vào sổ cái ngay khi nhận hàng

---

## 1.3. Ghi chú về cập nhật

| Thay đổi | Chi tiết |
|---------|---------|
| **Khấu hao tài sản** | Được chuyển sang module "Quản lý Tài chính" để tích hợp chặt chẽ với quy trình kế toán |
| **Đơn đề xuất mua + Duyệt mượn** | Thêm vào module "Quản lý Tài sản" để hoàn chỉnh quy trình kiểm soát |
| **Dashboard Tài chính** | Giao diện card-based hiện đại với biểu đồ Chart.js trực quan |
| **Dự báo ngân sách** | Chức năng mới hỗ trợ lập kế hoạch tài chính dài hạn (*sắp có*) |
![Dashboard](./images/overview.png)
![Tình hình mượn trả](./images/borrowing.png)
![Loại tài sản](./images/loai-tai-san.png)
![Tài sản cụ thể](./images/tai-san-cu-the.png)
![Phân bổ tài sản](./images/phan-bo-tai-san.png)
![Khấu hao tài sản](./images/khau-hao-tai-san.png)
![Kiểm kê tài sản](./images/kiem-ke-tai-san.png)
![Luân chuyển tài sản](./images/luan-chuyen-tai-san.png)
![Thanh lý tài sản](./images/thanh-ly-tai-san.png)
![Quản lý mượn tài sản](./images/don-muon-tai-san.png)
![Quản lý cấp phát tài sản](./images/cap-phat-tai-san.png)

# 2. Cài đặt công cụ, môi trường và các thư viện cần thiết

## 2.1. Clone project.

```
git clone https://github.com/nguyenngocdantruong/TTDN-15-04-N6.git
git checkout 
```

## 2.2. cài đặt các thư viện cần thiết

Người sử dụng thực thi các lệnh sau đề cài đặt các thư viện cần thiết

```
sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-distutils python3.10-dev build-essential libssl-dev libffi-dev zlib1g-dev python3.10-venv libpq-dev
```
## 2.3. khởi tạo môi trường ảo.

Thay đổi trình thông dịch sang môi trường ảo và chạy requirements.txt để cài đặt tiếp các thư viện được yêu cầu
```
python3.10 -m venv ./venv
```
```
source venv/bin/activate
```
```
pip3 install -r requirements.txt
```

# 3. Setup database

Khởi tạo database trên docker bằng việc thực thi file dockercompose.yml.
```
sudo apt install docker-compose
```
```
sudo docker-compose up -d
```

# 4. Setup tham số chạy cho hệ thống

## 4.1. Khởi tạo odoo.conf

Tạo tệp **odoo.conf** có nội dung như sau:

```
[options]
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5434
xmlrpc_port = 8069
```

# 5. Chạy hệ thống và cài đặt các ứng dụng cần thiết

Lệnh chạy
```
python3 odoo-bin.py -c odoo.conf -u all
```


Người sử dụng truy cập theo đường dẫn _http://localhost:8069/_ để đăng nhập vào hệ thống.

Hoàn tất
    
