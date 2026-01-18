# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


class KhauHaoTaiSan(models.Model):
    _name = 'khau_hao_tai_san'
    _description = 'Khấu hao tài sản'
    _rec_name = 'tai_san_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    tai_san_id = fields.Many2one('tai_san', string='Tài sản', required=True, ondelete='cascade')
    phe_duyet_mua_id = fields.Many2one('phe_duyet_mua_tai_san', string='Phê duyệt mua', readonly=True, ondelete='set null')
    ngay_bat_dau = fields.Date('Ngày bắt đầu khấu hao', required=True)
    gia_tri_ban_dau = fields.Float('Giá trị ban đầu')
    thoi_gian_khau_hao = fields.Integer('Thời gian khấu hao (năm)')
    ty_le_khau_hao = fields.Float('Tỷ lệ khấu hao (%/năm)')
    phuong_phap = fields.Selection([
        ('straight-line', 'Khấu hao tuyến tính'),
        ('degressive', 'Khấu hao giảm dần'),
        ('none', 'Không khấu hao')
    ], string='Phương pháp khấu hao')
    so_nam_khau_hao = fields.Integer('Số năm khấu hao', required=True)
    gia_tri_khau_hao_hang_nam = fields.Float('Giá trị khấu hao hàng năm', compute='_compute_gia_tri_khau_hao', store=True)
    tong_gia_tri_khau_hao = fields.Float('Tổng giá trị khấu hao', compute='_compute_tong_gia_tri', store=True)
    gia_tri_con_lai = fields.Float('Giá trị còn lại', compute='_compute_gia_tri_con_lai', store=True)
    trang_thai = fields.Selection([
        ('dang_khau_hao', 'Đang khấu hao'),
        ('tam_dung', 'Tạm dừng'),
        ('hoan_thanh', 'Hoàn thành')
    ], string='Trạng thái', default='dang_khau_hao')

    lich_khau_hao_ids = fields.One2many('lich_khau_hao', 'khau_hao_id', string='Lịch khấu hao')

    @api.depends('tai_san_id.gia_tri_ban_dau', 'so_nam_khau_hao')
    def _compute_gia_tri_khau_hao(self):
        for record in self:
            if record.tai_san_id and record.so_nam_khau_hao > 0:
                record.gia_tri_khau_hao_hang_nam = record.tai_san_id.gia_tri_ban_dau / record.so_nam_khau_hao
            else:
                record.gia_tri_khau_hao_hang_nam = 0

    @api.depends('gia_tri_khau_hao_hang_nam', 'so_nam_khau_hao')
    def _compute_tong_gia_tri(self):
        for record in self:
            record.tong_gia_tri_khau_hao = record.gia_tri_khau_hao_hang_nam * record.so_nam_khau_hao

    @api.depends('tai_san_id.gia_tri_ban_dau', 'tong_gia_tri_khau_hao')
    def _compute_gia_tri_con_lai(self):
        for record in self:
            record.gia_tri_con_lai = record.tai_san_id.gia_tri_ban_dau - record.tong_gia_tri_khau_hao

    @api.model
    def create(self, vals):
        record = super(KhauHaoTaiSan, self).create(vals)
        record._tao_lich_khau_hao()
        return record

    def _tao_lich_khau_hao(self):
        self.ensure_one()
        self.lich_khau_hao_ids.unlink()  # Xóa lịch cũ nếu có
        ngay_hien_tai = self.ngay_bat_dau
        for nam in range(1, self.so_nam_khau_hao + 1):
            self.env['lich_khau_hao'].create({
                'khau_hao_id': self.id,
                'nam': nam,
                'ngay_khau_hao': ngay_hien_tai,
                'gia_tri_khau_hao': self.gia_tri_khau_hao_hang_nam,
            })
            ngay_hien_tai = ngay_hien_tai + relativedelta(years=1)

    def action_tam_dung(self):
        self.trang_thai = 'tam_dung'

    def action_tiep_tuc(self):
        self.trang_thai = 'dang_khau_hao'


class LichKhauHao(models.Model):
    _name = 'lich_khau_hao'
    _description = 'Lịch khấu hao'

    khau_hao_id = fields.Many2one('khau_hao_tai_san', string='Khấu hao', ondelete='cascade')
    nam = fields.Integer('Năm')
    ngay_khau_hao = fields.Date('Ngày khấu hao')
    gia_tri_khau_hao = fields.Float('Giá trị khấu hao')
    da_ghi_nhan = fields.Boolean('Đã ghi nhận', default=False)