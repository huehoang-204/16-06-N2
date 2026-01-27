# 🤖 AI Chatbot Assistant - Tài liệu hướng dẫn

## Mục lục
1. [Tổng quan](#1-tổng-quan)
2. [Kiến trúc hệ thống](#2-kiến-trúc-hệ-thống)
3. [Cấu trúc file](#3-cấu-trúc-file)
4. [Backend - Python Models](#4-backend---python-models)
5. [Frontend - JavaScript & Templates](#5-frontend---javascript--templates)
6. [Tích hợp Gemini AI](#6-tích-hợp-gemini-ai)
7. [Cách hoạt động](#7-cách-hoạt-động)
8. [Hướng dẫn tùy chỉnh](#8-hướng-dẫn-tùy-chỉnh)

---

## 1. Tổng quan

### Giới thiệu
AI Chatbot Assistant là một trợ lý thông minh được tích hợp vào hệ thống Quản lý Tài sản và Tài chính Odoo. Chatbot sử dụng **Google Gemini AI** để cung cấp câu trả lời thông minh và hỗ trợ người dùng 24/7.

### Tính năng chính
- 💬 **Giao diện chat floating** - Widget chat nhỏ gọn ở góc phải màn hình
- 🤖 **AI-powered responses** - Sử dụng Gemini 2.0 Flash để sinh câu trả lời
- 📦 **Tích hợp hệ thống** - Truy vấn dữ liệu tài sản, mượn trả, bảo hành từ database
- 📋 **Hướng dẫn quy trình** - Cung cấp hướng dẫn step-by-step
- 💡 **Gợi ý thông minh** - Đưa ra các gợi ý phù hợp với context

---

## 2. Kiến trúc hệ thống

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (OWL)                         │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │ messenger_chat  │  │ messenger_chat  │                  │
│  │     .js         │  │     .xml        │                  │
│  └────────┬────────┘  └────────┬────────┘                  │
│           │                    │                           │
│           └────────┬───────────┘                           │
│                    │ ORM.call()                            │
└────────────────────┼───────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (Python)                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              chatbot.assistant                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │   │
│  │  │ process_    │  │ _detect_    │  │ _generate_  │  │   │
│  │  │ message()   │──▶│ intent()    │──▶│ response() │  │   │
│  │  └─────────────┘  └─────────────┘  └──────┬──────┘  │   │
│  │                                           │          │   │
│  │                    ┌──────────────────────┘          │   │
│  │                    ▼                                 │   │
│  │  ┌─────────────────────────────────────────────┐    │   │
│  │  │           _call_gemini_api()                │    │   │
│  │  │     (Google Gemini 2.0 Flash API)           │    │   │
│  │  └─────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ chatbot.         │  │ chatbot.         │                │
│  │ conversation     │  │ message          │                │
│  │ (Lưu hội thoại)  │  │ (Lưu tin nhắn)   │                │
│  └──────────────────┘  └──────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Cấu trúc file

```
q_trang_chu/
├── models/
│   └── chatbot.py              # Backend logic chính
├── static/
│   └── src/
│       ├── js/
│       │   └── messenger_chat.js    # Frontend OWL component
│       ├── xml/
│       │   └── messenger_chat.xml   # Template giao diện
│       └── css/
│           └── messenger_chat.css   # Styling
├── security/
│   └── ir.model.access.csv     # Phân quyền truy cập
└── __manifest__.py             # Đăng ký assets
```

---

## 4. Backend - Python Models

### 4.1. ChatbotConversation
Lưu trữ các cuộc hội thoại.

```python
class ChatbotConversation(models.Model):
    _name = 'chatbot.conversation'
    
    name = fields.Char('Tiêu đề', compute='_compute_name')
    user_id = fields.Many2one('res.users', 'Người dùng')
    message_ids = fields.One2many('chatbot.message', 'conversation_id')
    active = fields.Boolean(default=True)
```

### 4.2. ChatbotMessage
Lưu trữ từng tin nhắn trong cuộc hội thoại.

```python
class ChatbotMessage(models.Model):
    _name = 'chatbot.message'
    
    conversation_id = fields.Many2one('chatbot.conversation')
    content = fields.Text('Nội dung')
    is_user = fields.Boolean('Từ người dùng')
    timestamp = fields.Datetime('Thời gian')
    intent = fields.Char('Intent phát hiện')
```

### 4.3. ChatbotAssistant
Model chính xử lý logic chatbot.

**Phương thức quan trọng:**

| Method | Mô tả |
|--------|-------|
| `process_message()` | Xử lý tin nhắn từ user, gọi AI, trả response |
| `_detect_intent()` | Phát hiện ý định của người dùng |
| `_call_gemini_api()` | Gọi Google Gemini API |
| `_get_system_context()` | Lấy context từ database Odoo |
| `_generate_response()` | Fallback rule-based response |

---

## 5. Frontend - JavaScript & Templates

### 5.1. OWL Component (messenger_chat.js)

```javascript
class MessengerChat extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            isOpen: false,
            isTyping: false,
            messages: [],
            inputValue: "",
        });
    }

    async sendMessage(message) {
        // Gọi backend
        const response = await this.orm.call(
            "chatbot.assistant",
            "process_message",
            [message, this.state.currentConversationId]
        );
        
        // Hiển thị response
        this.state.messages.push({
            content: response.answer,
            isUser: false,
        });
    }
}
```

### 5.2. Template XML (messenger_chat.xml)

```xml
<t t-name="q_trang_chu.MessengerChat" owl="1">
    <div class="o_chatbot_container">
        <!-- Toggle Button -->
        <button class="o_chatbot_toggle_btn" t-on-click="toggleChat">🤖</button>
        
        <!-- Chat Window -->
        <div class="o_chatbot_window">
            <div class="o_chatbot_header">AI Assistant</div>
            <div class="o_chatbot_messages">
                <!-- Messages loop -->
            </div>
            <div class="o_chatbot_input_area">
                <input class="o_input_field" placeholder="Nhập tin nhắn..."/>
                <button class="o_input_send_btn">Gửi</button>
            </div>
        </div>
    </div>
</t>
```

---

## 6. Tích hợp Gemini AI

### 6.1. Cấu hình API

```python
GEMINI_API_KEY = "your-api-key"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
```

### 6.2. System Prompt

Chatbot được cấu hình với system prompt chi tiết:

```python
def _get_system_prompt(self):
    return """
    Bạn là AI Assistant - trợ lý thông minh 24/7 của hệ thống Quản lý Tài sản.
    
    🎯 Nhiệm vụ chính:
    1. Hướng dẫn người dùng quy trình mượn/trả tài sản
    2. Kiểm tra lịch trống của tài sản
    3. Tra cứu thông tin bảo hành
    4. Giải thích các quy định, chính sách
    
    📋 Quy tắc trả lời:
    - Trả lời ngắn gọn, rõ ràng bằng tiếng Việt
    - Sử dụng emoji phù hợp
    - Luôn thân thiện và chuyên nghiệp
    """
```

### 6.3. RAG (Retrieval-Augmented Generation)

Chatbot sử dụng kỹ thuật RAG để tăng độ chính xác:

```python
def _get_system_context(self, message, intent):
    context_parts = []
    
    # 1. Thông tin người dùng hiện tại
    user = self.env.user
    context_parts.append(f"Người dùng: {user.name}")
    
    # 2. Thống kê tài sản từ database
    TaiSan = self.env['tai_san']
    total_assets = TaiSan.search_count([])
    context_parts.append(f"Tổng số tài sản: {total_assets}")
    
    # 3. Tài sản có thể mượn
    available = self.env['phan_bo_tai_san'].search([...])
    
    # 4. Thông tin bảo hành
    # 5. Đơn mượn của người dùng
    
    return "\n".join(context_parts)
```

---

## 7. Cách hoạt động

### 7.1. Luồng xử lý tin nhắn

```
User gửi tin nhắn
        │
        ▼
┌───────────────────┐
│ 1. Detect Intent  │  Phân loại: muon_tai_san, bao_hanh, thanh_ly...
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ 2. Get Context    │  Lấy dữ liệu từ DB: tài sản, đơn mượn, user info
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ 3. Call Gemini    │  Gửi prompt + context → Gemini API
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ 4. Format & Save  │  Lưu tin nhắn vào DB, trả response
└────────┬──────────┘
         │
         ▼
    User nhận reply
```

### 7.2. Intent Detection

| Intent | Keywords | Ví dụ |
|--------|----------|-------|
| `muon_tai_san` | mượn, cho mượn, laptop, máy chiếu | "Làm sao mượn máy chiếu?" |
| `tra_tai_san` | trả, hoàn trả | "Tôi muốn trả tài sản" |
| `bao_hanh` | bảo hành, warranty | "Laptop còn bảo hành không?" |
| `thanh_ly` | thanh lý, xử lý tài sản cũ | "Quy trình thanh lý?" |
| `thong_ke` | thống kê, báo cáo | "Có bao nhiêu tài sản?" |

---

## 8. Hướng dẫn tùy chỉnh

### 8.1. Thay đổi API Key

Chỉnh sửa trong `models/chatbot.py`:

```python
GEMINI_API_KEY = "your-new-api-key"
```

### 8.2. Thêm Intent mới

```python
# Trong patterns dictionary
patterns = {
    ...
    'bao_tri': [
        r'bảo trì', r'sửa chữa', r'hỏng', r'lỗi'
    ],
}

# Thêm handler method
def _handle_bao_tri(self, message):
    return {
        'answer': "Hướng dẫn bảo trì tài sản...",
        'suggestions': ['Báo hỏng', 'Lịch bảo trì'],
    }
```

### 8.3. Thay đổi giao diện

Chỉnh sửa CSS trong `static/src/css/messenger_chat.css`:

```css
:root {
    --chat-primary: #2196F3;      /* Màu chính */
    --chat-primary-light: #E3F2FD; /* Màu nhạt */
    --chat-primary-dark: #1976D2;  /* Màu đậm */
}
```

### 8.4. Thêm Quick Reply buttons

Trong `static/src/js/messenger_chat.js`:

```javascript
this.welcomeOptions = [
    { label: "Mượn tài sản", query: "Làm sao để mượn tài sản?" },
    { label: "Kiểm tra bảo hành", query: "Laptop của tôi còn bảo hành?" },
    // Thêm option mới
    { label: "Báo hỏng", query: "Tôi muốn báo tài sản bị hỏng" },
];
```

---

## 📝 Ghi chú

- **Gemini API** yêu cầu kết nối internet
- **Fallback**: Nếu API fail, chatbot sẽ dùng rule-based response
- **Lịch sử chat** được lưu trong database, có thể xem lại
- **Phân quyền**: Tất cả users đều có thể sử dụng chatbot

---

## 📞 Liên hệ hỗ trợ

Nếu có vấn đề với chatbot, vui lòng liên hệ:
- **Email**: support@company.com
- **Slack**: #tech-support

---

*Tài liệu được cập nhật lần cuối: 28/01/2026*
