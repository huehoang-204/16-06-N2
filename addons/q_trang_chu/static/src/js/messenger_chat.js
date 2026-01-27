/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const { Component, useState, hooks } = owl;
const { onMounted } = hooks;

/**
 * AI Chatbot - Messenger-like Floating Widget
 */
class MessengerChat extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.user = useService("user");

        this.state = useState({
            isOpen: false,
            isTyping: false,
            messages: [],
            currentConversationId: null,
            inputValue: "",
        });

        this.welcomeOptions = [
            { label: "Mượn tài sản", query: "Làm sao để mượn tài sản?" },
            { label: "Kiểm tra bảo hành", query: "Laptop của tôi còn bảo hành bao lâu?" },
            { label: "Quy trình thanh lý", query: "Quy trình thanh lý tài sản cũ như thế nào?" },
            { label: "Thống kê tổng quan", query: "Cho tôi xem thống kê tổng quan" },
        ];

        onMounted(() => {
            console.log("MessengerChat mounted");
        });
    }

    toggleChat() {
        this.state.isOpen = !this.state.isOpen;
        if (this.state.isOpen && this.state.messages.length === 0) {
            this.addWelcomeMessage();
        }
    }

    addWelcomeMessage() {
        const userName = this.user.name || "bạn";
        this.state.messages.push({
            id: `welcome_${Date.now()}`,
            content: `Xin chào <strong>${userName}</strong>! 👋<br><br>Tôi là <strong>AI Assistant</strong> - trợ lý thông minh. Bạn cần hỗ trợ gì?`,
            isUser: false,
            timestamp: this.formatTime(new Date()),
            showOptions: true,
        });
    }

    closeChat() {
        this.state.isOpen = false;
    }

    async sendMessage(overrideMessage = null) {
        const message = overrideMessage || this.state.inputValue.trim();
        if (!message || this.state.isTyping) return;

        this.state.inputValue = "";

        this.state.messages.push({
            id: `user_${Date.now()}`,
            content: this.escapeHtml(message),
            isUser: true,
            timestamp: this.formatTime(new Date()),
        });
        this.scrollToBottom();

        this.state.isTyping = true;

        try {
            const response = await this.orm.call(
                "chatbot.assistant",
                "process_message",
                [message, this.state.currentConversationId]
            );

            this.state.currentConversationId = response.conversation_id;

            this.state.messages.push({
                id: `bot_${Date.now()}`,
                content: this.formatMarkdown(response.answer),
                isUser: false,
                timestamp: this.formatTime(new Date()),
                suggestions: response.suggestions || [],
            });

        } catch (error) {
            console.error("Chatbot error:", error);
            this.state.messages.push({
                id: `error_${Date.now()}`,
                content: "❌ Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại sau.",
                isUser: false,
                timestamp: this.formatTime(new Date()),
            });
        } finally {
            this.state.isTyping = false;
            this.scrollToBottom();
        }
    }

    sendQuickReply(text) {
        this.sendMessage(text);
    }

    handleOptionClick(option) {
        if (option.query) {
            this.sendMessage(option.query);
        } else if (option.label) {
            this.sendMessage(option.label);
        }
    }

    handleInput(event) {
        this.state.inputValue = event.target.value;
    }

    handleKeyPress(event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            this.sendMessage();
        }
    }

    scrollToBottom() {
        setTimeout(() => {
            const el = document.querySelector(".o_chatbot_messages");
            if (el) {
                el.scrollTop = el.scrollHeight;
            }
        }, 100);
    }

    formatTime(date) {
        return date.toLocaleTimeString("vi-VN", {
            hour: "2-digit",
            minute: "2-digit"
        });
    }

    formatMarkdown(text) {
        if (!text) return "";
        return text
            .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
            .replace(/\*(.*?)\*/g, "<em>$1</em>")
            .replace(/`([^`]+)`/g, "<code>$1</code>")
            .replace(/\n/g, "<br>");
    }

    escapeHtml(text) {
        const div = document.createElement("div");
        div.textContent = text;
        return div.innerHTML;
    }

    get userName() {
        return this.user.name || "bạn";
    }
}

MessengerChat.template = "q_trang_chu.MessengerChat";

// Register as floating widget
registry.category("main_components").add("MessengerChat", {
    Component: MessengerChat,
});
