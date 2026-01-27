# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json


class ChatbotController(http.Controller):
    """API Controller cho Chatbot"""

    @http.route('/chatbot/message', type='json', auth='user', methods=['POST'])
    def chatbot_message(self, message, conversation_id=None):
        """API endpoint xử lý tin nhắn chatbot"""
        result = request.env['chatbot.assistant'].process_message(message, conversation_id)
        return result

    @http.route('/chatbot/suggestions', type='json', auth='user', methods=['GET'])
    def chatbot_suggestions(self):
        """Lấy danh sách gợi ý câu hỏi"""
        faqs = request.env['chatbot.faq'].search([], limit=5, order='ask_count desc')
        return [{'question': faq.question, 'topic': faq.topic} for faq in faqs]

    @http.route('/dashboard/stats', type='json', auth='user', methods=['GET'])
    def dashboard_stats(self):
        """API endpoint lấy dữ liệu dashboard"""
        result = request.env['dashboard.main'].get_dashboard_data()
        return result

    @http.route('/dashboard/chart/<string:chart_type>', type='json', auth='user', methods=['GET'])
    def dashboard_chart(self, chart_type):
        """API endpoint lấy dữ liệu biểu đồ"""
        result = request.env['dashboard.main'].get_chart_data(chart_type)
        return result
