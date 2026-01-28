# Sơ đồ Kiến trúc Tổng thể Hệ thống (Mermaid Format)

## 1. Kiến trúc Tổng quan (High-Level Architecture)

```mermaid
flowchart TB
    subgraph CLIENTS["🖥️ CLIENTS"]
        WB["🌐 Web Browser<br/>Odoo Web UI"]
        MA["📱 Mobile App<br/>(Future)"]
        EA["💻 External App<br/>Node.js"]
        API["🔧 API Client<br/>Postman"]
    end

    subgraph DOCKER["🐳 DOCKER CONTAINERS"]
        subgraph ODOO["ODOO SERVER (odoo:15.0)"]
            subgraph WEB["WEB LAYER"]
                HTTP["HTTP Server<br/>(Werkzeug)"]
                JSONRPC["JSON-RPC<br/>API"]
                XMLRPC["XML-RPC<br/>API"]
                WS["WebSocket<br/>(Longpoll)"]
            end
            
            subgraph APP["APPLICATION LAYER"]
                ORM["ORM Framework"]
                MODULES["Custom Modules<br/>(4 Modules)"]
                EXT["External Services<br/>(Gemini API)"]
            end
        end
        
        subgraph DB["POSTGRESQL (postgres:10-alpine)"]
            DATABASE[("Database: btl2<br/>User: odoo<br/>Port: 5434")]
        end
    end

    CLIENTS --> |"HTTP/HTTPS<br/>Port: 8071"| WEB
    WEB --> APP
    APP --> DB

    style CLIENTS fill:#e1f5fe
    style DOCKER fill:#fff3e0
    style ODOO fill:#e8f5e9
    style DB fill:#fce4ec
```

## 2. Kiến trúc 4 Module

```mermaid
flowchart TB
    subgraph ADDONS["📦 CUSTOM ADDONS (/mnt/extra-addons)"]
        subgraph TRANGCHU["🏠 q_trang_chu (Trang chủ)"]
            TC_DASH["Dashboard Main"]
            TC_CHAT["AI Chatbot"]
            TC_KB["Knowledge Base"]
        end
        
        subgraph TAISAN["📋 quan_ly_tai_san (Quản lý Tài sản)"]
            TS_TS["Tài sản"]
            TS_PB["Phân bổ"]
            TS_DM["Đơn mượn"]
            TS_KK["Kiểm kê"]
            TS_TL["Thanh lý"]
        end
        
        subgraph TAICHINH["💰 quan_ly_tai_chinh (Quản lý Tài chính)"]
            TC_KH["Khấu hao"]
            TC_PD["Phê duyệt mua"]
            TC_BT["Bút toán"]
            TC_BC["Báo cáo"]
        end
        
        subgraph NHANSU["👥 nhan_su (Nhân sự)"]
            NS_NV["Nhân viên"]
            NS_PB["Phòng ban"]
            NS_CV["Chức vụ"]
            NS_LS["Lịch sử CT"]
        end
    end
    
    TC_CHAT --> |"Query Data"| TAISAN
    TC_CHAT --> |"Query Data"| TAICHINH
    TC_CHAT --> |"Query Data"| NHANSU
    TC_DASH --> |"Statistics"| TAISAN
    TC_DASH --> |"Statistics"| TAICHINH
    
    TAISAN --> |"FK: tai_san_id"| TAICHINH
    TAISAN --> |"FK: nhan_vien_id<br/>phong_ban_id"| NHANSU
    TAICHINH --> |"FK: phong_ban_id"| NHANSU

    style TRANGCHU fill:#e3f2fd
    style TAISAN fill:#e8f5e9
    style TAICHINH fill:#fff3e0
    style NHANSU fill:#fce4ec
```

## 3. Kiến trúc Kỹ thuật (3-Layer Architecture)

```mermaid
flowchart TB
    subgraph PRESENTATION["🎨 PRESENTATION LAYER"]
        OWL["OWL JS<br/>(Components)"]
        QWEB["QWeb/XML<br/>(Templates)"]
        CSS["SCSS/CSS<br/>(Styling)"]
        CHART["Chart.js<br/>(Charts)"]
    end
    
    subgraph BUSINESS["⚙️ BUSINESS LOGIC LAYER"]
        PY["Python 3.10"]
        ODOO_ORM["Odoo ORM"]
        CTRL["Controllers<br/>(HTTP Routes)"]
        WIZ["Wizards<br/>(Transient Models)"]
    end
    
    subgraph DATA["💾 DATA LAYER"]
        PG[("PostgreSQL 10")]
        
        subgraph TABLES["Tables (33 total)"]
            T1["nhan_su<br/>(4 tables)"]
            T2["quan_ly_tai_san<br/>(11 tables)"]
            T3["quan_ly_tai_chinh<br/>(6 tables)"]
            T4["q_trang_chu<br/>(12 tables)"]
        end
    end
    
    subgraph EXTERNAL["🌐 EXTERNAL SERVICES"]
        GEMINI["Google Gemini API<br/>AI/ML"]
    end
    
    PRESENTATION --> |"RPC Calls"| BUSINESS
    BUSINESS --> |"SQL Queries"| DATA
    BUSINESS --> |"HTTPS"| EXTERNAL
    PG --> TABLES

    style PRESENTATION fill:#e3f2fd
    style BUSINESS fill:#e8f5e9
    style DATA fill:#fff3e0
    style EXTERNAL fill:#f3e5f5
```

## 4. Kiến trúc Triển khai (Deployment)

```mermaid
flowchart TB
    subgraph HOST["🖥️ HOST MACHINE (Linux)"]
        subgraph DOCKER_ENGINE["🐳 DOCKER ENGINE"]
            subgraph COMPOSE["docker-compose.yml"]
                subgraph C_ODOO["Container: odoo_server"]
                    ODOO_IMG["Image: odoo:15.0"]
                    ODOO_PORT["Port: 8071:8069"]
                    ODOO_VOL["Volumes:<br/>• ./addons<br/>• odoo-docker.conf"]
                    ODOO_ENV["Env: GEMINI_API_KEY"]
                end
                
                subgraph C_PG["Container: postgres"]
                    PG_IMG["Image: postgres:10-alpine"]
                    PG_PORT["Port: 5434:5432"]
                    PG_VOL["Volume: database files"]
                    PG_ENV["Env: POSTGRES_*"]
                end
            end
        end
        
        subgraph FS["📁 FILE SYSTEM"]
            DIR1["/home/hue/btl2/16-06-N2/"]
            DIR2["├── addons/"]
            DIR3["├── docker-compose.yml"]
            DIR4["├── odoo-docker.conf"]
            DIR5["└── .env"]
        end
    end
    
    C_ODOO <--> |"Internal: 5432"| C_PG
    
    USER["👤 User Browser"]
    USER --> |"HTTP :8071"| C_ODOO
    
    GEMINI_EXT["☁️ Google Gemini API"]
    C_ODOO --> |"HTTPS"| GEMINI_EXT

    style HOST fill:#f5f5f5
    style DOCKER_ENGINE fill:#e3f2fd
    style C_ODOO fill:#e8f5e9
    style C_PG fill:#fff3e0
```

## 5. Luồng xử lý Chatbot (Sequence Diagram)

```mermaid
sequenceDiagram
    participant U as 👤 User
    participant OWL as 🎨 OWL Component
    participant PY as 🐍 ChatbotAssistant
    participant DB as 💾 PostgreSQL
    participant AI as 🤖 Gemini API

    U->>OWL: 1. Nhập tin nhắn
    OWL->>PY: 2. orm.call('process_message')
    
    PY->>PY: 3. Detect Intent
    PY->>DB: 4. Get Context (tai_san, phan_bo, ...)
    DB-->>PY: 5. Return Data
    
    PY->>DB: 6. Search Knowledge Base (FAQ, Policy)
    DB-->>PY: 7. Return Knowledge
    
    PY->>AI: 8. Call Gemini API with Context
    AI-->>PY: 9. AI Response
    
    PY->>DB: 10. Save Message
    PY-->>OWL: 11. Return Response
    OWL-->>U: 12. Hiển thị phản hồi
```

## 6. Luồng xử lý External API (Sequence Diagram)

```mermaid
sequenceDiagram
    participant EXT as 💻 External App (Node.js)
    participant RPC as 🔌 JSON-RPC Endpoint
    participant AUTH as 🔐 Authentication
    participant MODEL as 📋 Python Model
    participant DB as 💾 PostgreSQL

    EXT->>RPC: 1. POST /jsonrpc (authenticate)
    RPC->>AUTH: 2. common/login
    AUTH->>DB: 3. Verify credentials
    DB-->>AUTH: 4. User info
    AUTH-->>RPC: 5. Return UID
    RPC-->>EXT: 6. UID

    EXT->>RPC: 7. POST /jsonrpc (execute_kw)
    RPC->>MODEL: 8. nhan_vien.web_login()
    MODEL->>DB: 9. Query employee
    DB-->>MODEL: 10. Employee data
    MODEL-->>RPC: 11. Result
    RPC-->>EXT: 12. JSON Response
```

## 7. Sơ đồ Component

```mermaid
flowchart LR
    subgraph FRONTEND["Frontend (Browser)"]
        subgraph OWL_COMP["OWL Components"]
            DASH["DashboardMain"]
            CHAT["MessengerChat"]
            FORM["FormController"]
        end
        
        subgraph ASSETS["Static Assets"]
            JS["JavaScript"]
            CSS["CSS"]
            IMG["Images"]
        end
    end
    
    subgraph BACKEND["Backend (Python)"]
        subgraph MODELS["Models"]
            M1["tai_san"]
            M2["nhan_vien"]
            M3["chatbot_assistant"]
            M4["khau_hao_tai_san"]
        end
        
        subgraph CONTROLLERS["Controllers"]
            C1["Main Controller"]
            C2["Chatbot Controller"]
        end
        
        subgraph VIEWS["Views (XML)"]
            V1["Form Views"]
            V2["Tree Views"]
            V3["Kanban Views"]
        end
    end
    
    OWL_COMP --> |"RPC"| CONTROLLERS
    CONTROLLERS --> MODELS
    VIEWS --> OWL_COMP
    
    style FRONTEND fill:#e3f2fd
    style BACKEND fill:#e8f5e9
```

## 8. Sơ đồ Database (ER Overview)

```mermaid
erDiagram
    NHAN_VIEN ||--o{ PHAN_BO_TAI_SAN : "uses"
    NHAN_VIEN ||--o{ DON_MUON_TAI_SAN : "borrows"
    PHONG_BAN ||--o{ PHAN_BO_TAI_SAN : "manages"
    PHONG_BAN ||--o{ DE_XUAT_MUA_TAI_SAN : "requests"
    
    TAI_SAN ||--o{ PHAN_BO_TAI_SAN : "allocated"
    TAI_SAN ||--o{ KHAU_HAO_TAI_SAN : "depreciated"
    TAI_SAN ||--o{ THANH_LY_TAI_SAN : "disposed"
    
    DANH_MUC_TAI_SAN ||--o{ TAI_SAN : "contains"
    
    DE_XUAT_MUA_TAI_SAN ||--o{ PHE_DUYET_MUA_TAI_SAN : "approved"
    PHE_DUYET_MUA_TAI_SAN ||--o{ KHAU_HAO_TAI_SAN : "creates"
    KHAU_HAO_TAI_SAN ||--o{ BUT_TOAN : "generates"
    
    RES_USERS ||--o{ CHATBOT_CONVERSATION : "owns"
    CHATBOT_CONVERSATION ||--o{ CHATBOT_MESSAGE : "contains"
```

## 9. Tóm tắt Công nghệ

```mermaid
mindmap
  root((Hệ thống<br/>Quản lý<br/>Tài sản))
    Frontend
      OWL JS
      QWeb Templates
      SCSS/CSS
      Chart.js
    Backend
      Python 3.10
      Odoo 15.0
      ORM Framework
    Database
      PostgreSQL 10
      33 Tables
    DevOps
      Docker
      Docker Compose
    External
      Google Gemini API
    Modules
      Nhân sự 4 tables
      Tài sản 11 tables
      Tài chính 6 tables
      Trang chủ 12 tables
```

## 10. Thông tin Triển khai

| Component | Technology | Version | Port |
|-----------|------------|---------|------|
| Web Server | Odoo | 15.0 | 8071 |
| Database | PostgreSQL | 10-alpine | 5434 |
| Container | Docker | Latest | - |
| AI Service | Google Gemini | 1.5-flash | - |

| Module | Tables | Description |
|--------|--------|-------------|
| `nhan_su` | 4 | Quản lý nhân viên, phòng ban, chức vụ |
| `quan_ly_tai_san` | 11 | Quản lý tài sản, phân bổ, mượn trả |
| `quan_ly_tai_chinh` | 6 | Khấu hao, phê duyệt, bút toán |
| `q_trang_chu` | 12 | Dashboard, AI Chatbot |
| **Total** | **33** | |
