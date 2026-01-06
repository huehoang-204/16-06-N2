# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ButToan(models.Model):
    _name = 'but_toan'
    _description = 'Bút toán kế toán'
    _rec_name = 'so_but_toan'

    so_but_toan = fields.Char('Số bút toán', required=True, default=lambda self: self._default_so_but_toan())
    ngay_but_toan = fields.Date('Ngày bút toán', required=True, default=fields.Date.today)
    mo_ta = fields.Text('Mô tả')
    khau_hao_id = fields.Many2one('khau_hao_tai_san', string='Khấu hao tài sản', ondelete='cascade')
    tai_khoan_no_id = fields.Many2one('account.account', string='Tài khoản nợ', required=True)
    tai_khoan_co_id = fields.Many2one('account.account', string='Tài khoản có', required=True)
    so_tien = fields.Float('Số tiền', required=True)
    trang_thai = fields.Selection([
        ('draft', 'Dự thảo'),
        ('posted', 'Đã vào sổ')
    ], string='Trạng thái', default='draft')

    @api.model
    def _default_so_but_toan(self):
        return self.env['ir.sequence'].next_by_code('but_toan.sequence') or 'BT001'

    def action_post(self):
        if self.trang_thai == 'draft':
            self.trang_thai = 'posted'
            # Tạo journal entry thực tế nếu cần (tích hợp với accounting module)
            # self._create_journal_entry()

    def action_draft(self):
        if self.trang_thai == 'posted':
            self.trang_thai = 'draft'

    # def _create_journal_entry(self):
    #     # Logic tạo journal entry trong Odoo accounting
    #     pass