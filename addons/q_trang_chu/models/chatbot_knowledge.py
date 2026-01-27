# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ChatbotKnowledge(models.Model):
    """Knowledge Base cho Chatbot - RAG System"""
    _name = 'chatbot.knowledge'
    _description = 'Cơ sở tri thức Chatbot'
    _order = 'sequence, id'

    name = fields.Char('Mã', required=True)
    title = fields.Char('Tiêu đề', required=True)
    topic = fields.Selection([
        ('muon_tai_san', 'Mượn tài sản'),
        ('tra_tai_san', 'Trả tài sản'),
        ('bao_hanh', 'Bảo hành'),
        ('thanh_ly', 'Thanh lý'),
        ('khau_hao', 'Khấu hao'),
        ('quy_trinh', 'Quy trình'),
        ('faq', 'FAQ'),
        ('other', 'Khác'),
    ], string='Chủ đề', required=True, default='faq')
    
    content = fields.Html('Nội dung', required=True)
    content_text = fields.Text('Nội dung text', compute='_compute_content_text', store=True)
    keywords = fields.Char('Từ khóa', help='Các từ khóa cách nhau bằng dấu phẩy')
    
    sequence = fields.Integer('Thứ tự', default=10)
    active = fields.Boolean(default=True)
    
    # Thống kê
    view_count = fields.Integer('Lượt xem', default=0)
    helpful_count = fields.Integer('Hữu ích', default=0)
    
    @api.depends('content')
    def _compute_content_text(self):
        import re
        for record in self:
            if record.content:
                # Loại bỏ HTML tags
                record.content_text = re.sub('<[^<]+?>', '', record.content)
            else:
                record.content_text = ''

    def action_mark_helpful(self):
        """Đánh dấu bài viết hữu ích"""
        self.helpful_count += 1

    def action_increment_view(self):
        """Tăng lượt xem"""
        self.view_count += 1


class ChatbotFAQ(models.Model):
    """FAQ - Câu hỏi thường gặp"""
    _name = 'chatbot.faq'
    _description = 'Câu hỏi thường gặp'
    _order = 'sequence, id'

    question = fields.Char('Câu hỏi', required=True)
    answer = fields.Html('Câu trả lời', required=True)
    topic = fields.Selection([
        ('muon_tai_san', 'Mượn tài sản'),
        ('tra_tai_san', 'Trả tài sản'),
        ('bao_hanh', 'Bảo hành'),
        ('thanh_ly', 'Thanh lý'),
        ('khau_hao', 'Khấu hao'),
        ('quy_trinh', 'Quy trình'),
        ('other', 'Khác'),
    ], string='Chủ đề', required=True, default='other')
    
    keywords = fields.Char('Từ khóa liên quan')
    sequence = fields.Integer('Thứ tự', default=10)
    active = fields.Boolean(default=True)
    
    # Thống kê
    ask_count = fields.Integer('Số lần hỏi', default=0)


class ChatbotPolicy(models.Model):
    """Quy chế, quy định"""
    _name = 'chatbot.policy'
    _description = 'Quy chế, quy định'
    _order = 'sequence, id'

    name = fields.Char('Tên quy chế', required=True)
    code = fields.Char('Mã số')
    content = fields.Html('Nội dung', required=True)
    summary = fields.Text('Tóm tắt')
    
    category = fields.Selection([
        ('tai_san', 'Quản lý tài sản'),
        ('muon_tra', 'Mượn trả'),
        ('thanh_ly', 'Thanh lý'),
        ('bao_tri', 'Bảo trì'),
        ('tai_chinh', 'Tài chính'),
        ('other', 'Khác'),
    ], string='Phân loại', required=True, default='other')
    
    effective_date = fields.Date('Ngày hiệu lực')
    expiry_date = fields.Date('Ngày hết hiệu lực')
    
    attachment_ids = fields.Many2many('ir.attachment', string='Tài liệu đính kèm')
    
    sequence = fields.Integer('Thứ tự', default=10)
    active = fields.Boolean(default=True)
