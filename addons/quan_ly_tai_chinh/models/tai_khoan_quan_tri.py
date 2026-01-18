# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date


class TaiKhoanQuanTri(models.Model):
    _name = 'tai_khoan_quan_tri'
    _description = 'Tài khoản quản trị'
    _rec_name = 'ten_tai_khoan'

    ten_tai_khoan = fields.Char('Tên tài khoản', required=True)
    ma_tai_khoan = fields.Char('Mã tài khoản', required=True)
    phong_ban_id = fields.Many2one('phong_ban', string='Phòng ban', required=False, ondelete='set null')
    
    # Thêm field liên kết phê duyệt mua
    phe_duyet_mua_id = fields.Many2one('phe_duyet_mua_tai_san', string='Phê duyệt mua', readonly=True, ondelete='cascade')
    ngay_ghi_nhan = fields.Date('Ngày ghi nhận')
    loai_giao_dich = fields.Selection([
        ('mua_tai_san', 'Mua tài sản'),
        ('thanh_ly', 'Thanh lý'),
        ('khau_hao', 'Khấu hao'),
        ('khac', 'Khác')
    ], string='Loại giao dịch')
    mo_ta = fields.Text('Mô tả')
    so_tien = fields.Float('Số tiền')
    don_vi_tien_te = fields.Selection([
        ('vnd', 'VNĐ'),
        ('usd', 'USD'),
    ], string='Đơn vị tiền tệ')
    
    # THAY ĐỔI: XÓA store=True tạm thời
    tong_chi_phi_khau_hao = fields.Float('Tổng chi phí khấu hao', compute='_compute_tong_chi_phi')
    chi_phi_thang_nay = fields.Float('Chi phí tháng này', compute='_compute_chi_phi_thang_nay')

    @api.depends('phong_ban_id')
    def _compute_tong_chi_phi(self):
        for record in self:
            try:
                # KIỂM TRA xem field có tồn tại không
                TaiSan = self.env['tai_san']
                
                # Cách 1: Kiểm tra bằng hasattr
                if hasattr(TaiSan, '_fields') and 'phong_ban_id' in TaiSan._fields:
                    tai_san_ids = TaiSan.search([('phong_ban_id', '=', record.phong_ban_id.id)])
                else:
                    # Nếu không có field phong_ban_id, tìm tất cả tài sản
                    tai_san_ids = TaiSan.search([])
                
                # Kiểm tra model khau_hao_tai_san có tồn tại không
                if 'khau_hao_tai_san' in self.env:
                    khau_hao_ids = self.env['khau_hao_tai_san'].search([('tai_san_id', 'in', tai_san_ids.ids)])
                    record.tong_chi_phi_khau_hao = sum(khau_hao.tong_gia_tri_khau_hao for khau_hao in khau_hao_ids)
                else:
                    record.tong_chi_phi_khau_hao = 0.0
                    
            except Exception as e:
                # Nếu có lỗi, đặt giá trị mặc định
                record.tong_chi_phi_khau_hao = 0.0
                # Có thể log lỗi nếu cần
                # _logger.error("Error computing tong_chi_phi_khau_hao: %s", str(e))

    @api.depends('phong_ban_id')
    def _compute_chi_phi_thang_nay(self):
        for record in self:
            try:
                thang_hien_tai = fields.Date.today().month
                nam_hien_tai = fields.Date.today().year
                
                TaiSan = self.env['tai_san']
                
                # Kiểm tra field
                if hasattr(TaiSan, '_fields') and 'phong_ban_id' in TaiSan._fields:
                    tai_san_ids = TaiSan.search([('phong_ban_id', '=', record.phong_ban_id.id)])
                else:
                    tai_san_ids = TaiSan.search([])
                
                chi_phi_thang = 0
                
                # Kiểm tra các model có tồn tại không
                if 'khau_hao_tai_san' in self.env and 'lich_khau_hao' in self.env:
                    khau_hao_ids = self.env['khau_hao_tai_san'].search([('tai_san_id', 'in', tai_san_ids.ids)])
                    
                    for khau_hao in khau_hao_ids:
                        lich_khau_hao = self.env['lich_khau_hao'].search([
                            ('khau_hao_id', '=', khau_hao.id),
                            ('ngay_khau_hao', '>=', date(nam_hien_tai, thang_hien_tai, 1)),
                            ('ngay_khau_hao', '<', date(nam_hien_tai, thang_hien_tai + 1, 1) if thang_hien_tai < 12 else date(nam_hien_tai + 1, 1, 1))
                        ])
                        chi_phi_thang += sum(lich.gia_tri_khau_hao / 12 for lich in lich_khau_hao)
                
                record.chi_phi_thang_nay = chi_phi_thang
                
            except Exception as e:
                record.chi_phi_thang_nay = 0.0
                # _logger.error("Error computing chi_phi_thang_nay: %s", str(e))