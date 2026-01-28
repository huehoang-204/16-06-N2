<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>

<h2 align="center">
    Youth Union Member Management
</h2>
<div align="center">
    <p align="center">
        <img width="170" alt="image" src="https://github.com/user-attachments/assets/e5cf9d51-47fb-42d2-b5df-fb3d2e669772" />
        <img width="180"  alt="image" src="https://github.com/user-attachments/assets/1a21a890-24d3-4481-b8ca-7885637bf17e" />
        <img width="200" alt="image" src="https://github.com/user-attachments/assets/4901129c-be54-4246-9478-2847c45a48bd" />
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)

</div>

---
## 🔧 Các công nghệ được sử dụng

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
<img width="861" height="834" alt="image" src="https://github.com/user-attachments/assets/5d08646a-4d6c-4bd7-b8a7-485f2723d589" />

---

## 1.2. Các chức năng chính

### **Module Quản lý Tài sản**

#### 1. Dashboard tổng quan và tình hình mượn trả
Cung cấp cái nhìn 360° về tình trạng tài sản của tổ chức:
- Số lượng tài sản hiện có trong hệ thống
- Số lượng tài sản đang bị lỗi/hư hỏng
- Dự báo nhu cầu mua sắm trong tương lai
<img width="1258" height="809" alt="image" src="https://github.com/user-attachments/assets/f0aa82cf-27c6-4910-88ba-7d45d1c07bdd" />
<img width="1248" height="678" alt="image" src="https://github.com/user-attachments/assets/393a8521-5874-4137-b803-1fef6e6cc231" />


#### 2. Quản lý loại tài sản
Chuẩn hóa phân loại tài sản trong toàn tổ chức:
- Tối ưu hóa quy trình kế toán - không cần định khoản lại cho mỗi lần mua mới
- Tự động áp dụng chính sách khấu hao tiêu chuẩn (vd: Laptop → khấu hao 3 năm → TK 211)
- Đảm bảo nhất quán dữ liệu và báo cáo
![Tình hình mượn trả](./images/borrowing.png)
![Loại tài sản](./images/loai-tai-san.png)
#### 3. Quản lý tài sản cụ thể
Xây dựng "hồ sơ lý lịch" chi tiết cho từng tài sản (Digital Twin):
- Theo dõi Serial Number, Model, nhà cung cấp
- Lưu trữ lịch sử bảo trì, sửa chữa
- Ghi nhận giá trị khấu hao và tuổi thọ
- Tạo QR Code cho quản lý hàng tồn kho
![Tài sản cụ thể](./images/tai-san-cu-the.png)

#### 4. Phân bổ tài sản cho các phòng ban
Xác định rõ ràng trách nhiệm vật lý và tài chính:
- Tài sản nằm ở phòng nào → phòng đó chịu trách nhiệm bảo quản
- Phân bổ chi phí khấu hao theo đơn vị sử dụng
- Thuận lợi cho báo cáo chi phí theo bộ phận
![Phân bổ tài sản](./images/phan-bo-tai-san.png)
![Khấu hao tài sản](./images/khau-hao-tai-san.png)
#### 5. Kiểm kê tài sản
Đối chiếu định kỳ giữa "Phần mềm" (hệ thống) và "Thực tế" (kho):
- Phát hiện tài sản mất mát, hư hỏng hoặc thất thoát
- Điều chỉnh sổ sách khi có chênh lệch
- Đảm bảo độ chính xác của dữ liệu tài chính
![Kiểm kê tài sản](./images/kiem-ke-tai-san.png)

#### 6. Luân chuyển tài sản
Linh hoạt trong quản lý nhân sự và cơ cấu tổ chức:
- Chuyển tài sản giữa nhân viên khi có thay đổi nhân sự
- Chuyển tài sản giữa các chi nhánh/phòng ban
- Duy trì lịch sử luân chuyển để kiểm toán
![Luân chuyển tài sản](./images/luan-chuyen-tai-san.png)

#### 7. Thanh lý tài sản
Xử lý tài sản hết giá trị sử dụng:
- Ghi nhận tài sản hư hỏng không thể sửa chữa
- Thu hồi vốn nếu bán được
- Làm sạch sổ sách kế toán
![Thanh lý tài sản](./images/thanh-ly-tai-san.png)

#### 8. Quản lý đơn mượn tài sản & cấp phát tài sản
Quy trình hóa việc yêu cầu/cấp phát thiết bị:
- Tránh cấp phát tùy tiện, không có kiểm soát
- Theo dõi tài sản được mượn/cấp và thời hạn trả
- Đảm bảo tuân thủ ngân sách và chính sách
![Quản lý mượn tài sản](./images/don-muon-tai-san.png)

#### 9. Đơn đề xuất mua tài sản & Duyệt đơn mượn **(NEW)**
Kiểm soát và phê duyệt các yêu cầu:
- Tạo và theo dõi đơn đề xuất mua sắm tài sản
- Workflow phê duyệt rõ ràng từ lập đơn → duyệt → thực hiện mua
- Duyệt/từ chối yêu cầu mượn tài sản theo quy định
![Quản lý cấp phát tài sản](./images/cap-phat-tai-san.png)
---

### **Module Quản lý Tài chính**

#### 1. Dashboard tài chính
Giao diện tổng hợp với thiết kế card-based hiện đại:
- **Thống kê phê duyệt**: Tổng, chờ duyệt, đã duyệt, hoàn thành, từ chối
- **Thống kê khấu hao**: Tổng tài sản, đang khấu hao, giá trị còn lại
- **Khấu hao theo thời kỳ**: Tháng này, quý này, năm nay (tính từ dữ liệu thực)
- **Thống kê bút toán**: Tổng, đã ghi nhận, nhập, giá trị toàn bộ
- **Thống kê kế toán quản trị**: Tổng chi phí, chi phí tháng hiện tại
- **Biểu đồ động**: 4 loại biểu đồ trực quan lấy dữ liệu thực từ database
  - Doughnut chart: Trạng thái phê duyệt
  - Bar chart: Trạng thái tài sản
  - Line chart: Xu hướng khấu hao 12 tháng
  - Line chart: Xu hướng mua sắm 12 tháng
- Nút action nhanh để điều hướng đến danh sách liên quan
<img width="1202" height="847" alt="image" src="https://github.com/user-attachments/assets/c79b1483-3c62-4648-850e-d70d9957086e" />
<img width="1184" height="847" alt="image" src="https://github.com/user-attachments/assets/f0f04ab9-3ead-4158-b6e6-6e87d27b99bf" />

#### 2. Khấu hao tài sản
Phân bổ chi phí mua tài sản vào nhiều kỳ kế toán:
- Tuân thủ nguyên tắc "Phù hợp" của kế toán
- Tính toán khấu hao theo phương pháp đường thẳng
- Tự động sinh bút toán khấu hao hàng kỳ
<img width="1747" height="393" alt="image" src="https://github.com/user-attachments/assets/9c7512aa-364f-4fa9-8311-6c741a73caf7" />


#### 3. Bút toán khấu hao
Hành động pháp lý để ghi nhận chi phí vào Sổ cái:
- Không có bút toán → báo cáo tài chính sai
- Tự động tạo bút toán khấu hao từ lịch khấu hao
- Kiểm soát các bút toán theo trạng thái (Nháp, Đã ghi nhận)
<img width="1740" height="435" alt="image" src="https://github.com/user-attachments/assets/12aa559b-c033-4811-b686-02a5c059e89c" />


#### 4. Tài khoản quản trị
Phân bổ chi phí theo bộ phận:
- Ghi nhận chi phí vận hành từng phòng ban
- Phân tích "Chi phí này của bộ phận nào?"
- Hỗ trợ báo cáo chi phí theo đơn vị
<img width="1737" height="242" alt="image" src="https://github.com/user-attachments/assets/2652593c-36c8-446d-86e3-88ad4d57a75a" />


#### 5. Báo cáo tài chính
Tạo các báo cáo tuân thủ tiêu chuẩn kế toán:
- Bảng cân đối kế toán
- Báo cáo kết quả kinh doanh
- Báo cáo dòng tiền
- Chi tiết khấu hao và giá trị tài sản
<img width="1735" height="225" alt="image" src="https://github.com/user-attachments/assets/9a82d305-d0c1-40b4-ba5f-5edd20a6e92a" />




#### 7. Quản lý đơn mua tài sản
Theo dõi toàn bộ quy trình mua sắm:
- Từ đơn đề xuất → phê duyệt → hợp đồng → nhận hàng → thanh toán
- Liên kết với kế toán cho phép ghi nhận tài sản vào sổ cái ngay khi nhận hàng
<img width="1731" height="264" alt="image" src="https://github.com/user-attachments/assets/e8dc681c-ef1a-4cda-83d0-d112860e5d63" />
<img width="1708" height="830" alt="image" src="https://github.com/user-attachments/assets/446cd444-22e9-47b3-9e50-1ed41d3b94eb" />

---

### **Module Trang Chủ (q_trang_chu)** **(NEW)**

#### 1. Dashboard tổng quan
Giao diện chính của hệ thống với các thống kê tổng hợp:
- **Thống kê tài sản**: Tổng số, đang hoạt động, tỉ lệ sử dụng
- **Thống kê mượn trả**: Đơn chờ duyệt, đang mượn, quá hạn
- **Thao tác nhanh**: Các nút điều hướng đến chức năng chính
- Tự động tính toán dữ liệu khi mở dashboard
<img width="1423" height="836" alt="image" src="https://github.com/user-attachments/assets/2122923c-2915-4fb9-b0f2-488734e64d45" />

#### 2. AI Chatbot Assistant 🤖 **(NEW)**
Trợ lý thông minh tích hợp **Google Gemini AI**:
- **Giao diện floating widget** - Nút chat ở góc phải màn hình
- **Hỗ trợ 24/7** với các tính năng:
  - 📦 Hướng dẫn quy trình mượn/trả tài sản step-by-step
  - 📅 Kiểm tra lịch trống của tài sản
  - 🔧 Tra cứu thông tin bảo hành từ database
  - 📋 Giải thích các quy định, chính sách quản lý
  - 📊 Cung cấp thống kê nhanh
- **Tích hợp RAG** (Retrieval-Augmented Generation):
  - Tự động lấy context từ database Odoo
  - Hiểu thông tin người dùng, phòng ban, tài sản đang quản lý
- **Intent Detection**: Tự động phát hiện ý định người dùng
- **Lưu lịch sử hội thoại** trong database
<img width="1713" height="860" alt="image" src="https://github.com/user-attachments/assets/182cceaf-e288-4b74-a413-8e92f3eccd98" />

> 📖 Chi tiết xem tại: `addons/q_trang_chu/CHATBOT_DOCUMENTATION.md`
#### 3. Quản lý chatbot
<img width="1724" height="278" alt="image" src="https://github.com/user-attachments/assets/452b0160-52a7-4a27-9e62-fb43a984f237" />
<img width="1724" height="270" alt="image" src="https://github.com/user-attachments/assets/ad116968-880f-414c-974f-e3846ba25811" />
<img width="1706" height="333" alt="image" src="https://github.com/user-attachments/assets/a817860e-fd39-4939-975c-9e2eff5f4e40" />

---

## 1.3. Ghi chú về cập nhật

| Thay đổi | Chi tiết |
|---------|---------|
| **Khấu hao tài sản** | Được chuyển sang module "Quản lý Tài chính" để tích hợp chặt chẽ với quy trình kế toán |
| **Đơn đề xuất mua + Duyệt mượn** | Thêm vào module "Quản lý Tài sản" để hoàn chỉnh quy trình kiểm soát |
| **Dashboard Tài chính** | Giao diện card-based hiện đại với biểu đồ Chart.js động lấy dữ liệu từ database |
| **Dashboard Tài sản** | Redesign giao diện với CSS Grid, responsive và đồng bộ style |
| **AI Chatbot** | Tích hợp Google Gemini 2.0 Flash với RAG để hỗ trợ người dùng thông minh |
| **Biểu đồ động** | Biểu đồ xu hướng khấu hao và mua sắm tự động cập nhật từ database |

### Cập nhật kỹ thuật (28/01/2026)
- ✅ Sửa logic tính toán dashboard tài chính (sử dụng model `but_toan` thay vì `account.move`)
- ✅ Thêm tính năng khấu hao theo thời kỳ (tháng/quý/năm)
- ✅ Biểu đồ Chart.js lấy dữ liệu động qua JSON-RPC API
- ✅ Cải thiện CSS cho dashboard cards (equal height, responsive)
- ✅ Chatbot với giao diện Messenger-like và tích hợp Gemini AI


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

## 4.2. Cấu hình Gemini API Key (cho AI Chatbot)

Để sử dụng tính năng AI Chatbot, bạn cần có API key từ Google Gemini:

1. **Lấy API key** tại: https://aistudio.google.com/apikey

2. **Tạo file `.env`** từ file mẫu:
```bash
cp .env.example .env
```

3. **Điền API key** vào file `.env`:
```
GEMINI_API_KEY=your-actual-api-key-here
```

4. **Xuất biến môi trường** trước khi chạy Odoo:
```bash
export GEMINI_API_KEY="your-actual-api-key-here"
```

> ⚠️ **Lưu ý bảo mật**: File `.env` đã được thêm vào `.gitignore` và sẽ KHÔNG được push lên Git.

# 5. Chạy hệ thống và cài đặt các ứng dụng cần thiết

## 5.1. Chạy Odoo server

```bash
# Kích hoạt môi trường ảo (nếu chưa)
source venv/bin/activate

# Xuất biến môi trường cho Gemini AI
export GEMINI_API_KEY="your-api-key"

# Chạy Odoo
python3 odoo-bin -c odoo.conf -u all
```

## 5.2. Truy cập hệ thống

Người sử dụng truy cập theo đường dẫn: **http://localhost:8069/**

Đăng nhập với tài khoản admin mặc định và cài đặt các module cần thiết:
- `q_trang_chu` - Trang chủ & AI Chatbot
- `quan_ly_tai_san` - Quản lý Tài sản
- `quan_ly_tai_chinh` - Quản lý Tài chính

---

## 📚 Tài liệu bổ sung

| Tài liệu | Đường dẫn |
|----------|-----------|
| Hướng dẫn Chatbot | `addons/q_trang_chu/CHATBOT_DOCUMENTATION.md` |

---

**Hoàn tất!** 🎉
