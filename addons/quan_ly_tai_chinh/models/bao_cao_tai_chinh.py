# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime, timedelta
import json


class BaoCaoTaiChinh(models.Model):
    _name = 'bao_cao_tai_chinh'
    _description = 'Báo cáo tài chính'
    _rec_name = 'name'
    _order = 'nam desc, thang desc'
    
    # ========== THÔNG TIN CHUNG ==========
    name = fields.Char(string='Tên báo cáo', required=True, copy=False)
    thang = fields.Integer(string='Tháng', required=True, default=lambda self: datetime.now().month)
    nam = fields.Integer(string='Năm', required=True, default=lambda self: datetime.now().year)
    
    # ========== TRẠNG THÁI ==========
    trang_thai = fields.Selection([
        ('draft', 'Nháp'),
        ('in_progress', 'Đang xử lý'),
        ('completed', 'Hoàn thành'),
        ('cancelled', 'Hủy')
    ], string='Trạng thái', default='draft', tracking=True)
    
    # ========== DOANH THU VÀ LỢI NHUẬN ==========
    doanh_thu = fields.Float(string='Doanh thu', default=0.0)
    tong_chi_phi = fields.Float(string='Tổng chi phí', compute='_compute_tong_chi_phi', store=True)
    loi_nhuan = fields.Float(string='Lợi nhuận', compute='_compute_loi_nhuan', store=True)
    ty_le_loi_nhuan = fields.Float(string='Tỷ lệ lợi nhuận (%)', compute='_compute_ty_le_loi_nhuan', store=True)
    
    # ========== CHI TIẾT CHI PHÍ ==========
    chi_phi_khau_hao = fields.Float(string='Chi phí khấu hao', default=0.0)
    chi_phi_luong = fields.Float(string='Chi phí lương', default=0.0)
    chi_phi_van_phong = fields.Float(string='Chi phí văn phòng', default=0.0)
    chi_phi_marketing = fields.Float(string='Chi phí Marketing', default=0.0)
    chi_phi_dien_nuoc = fields.Float(string='Chi phí điện nước', default=0.0)
    chi_phi_khac = fields.Float(string='Chi phí khác', default=0.0)
    
    # ========== THÔNG TIN THEO DÕI ==========
    ngay_tao = fields.Datetime(string='Ngày tạo', default=fields.Datetime.now, readonly=True)
    ngay_hoan_thanh = fields.Datetime(string='Ngày hoàn thành', readonly=True)
    nguoi_tao_id = fields.Many2one('res.users', string='Người tạo', default=lambda self: self.env.user, readonly=True)
    nguoi_xu_ly_id = fields.Many2one('res.users', string='Người xử lý', readonly=True)
    
    # ========== DỮ LIỆU BIỂU ĐỒ ==========
    bieu_do_du_lieu = fields.Text(string='Dữ liệu biểu đồ', compute='_compute_bieu_do_du_lieu', store=False)
    bieu_do_phan_bo_chi_phi = fields.Text(string='Phân bổ chi phí', compute='_compute_bieu_do_phan_bo_chi_phi', store=False)
    
    # ========== COMPUTE METHODS ==========
    @api.depends('chi_phi_khau_hao', 'chi_phi_luong', 'chi_phi_van_phong', 
                 'chi_phi_marketing', 'chi_phi_dien_nuoc', 'chi_phi_khac')
    def _compute_tong_chi_phi(self):
        for record in self:
            record.tong_chi_phi = (
                record.chi_phi_khau_hao +
                record.chi_phi_luong +
                record.chi_phi_van_phong +
                record.chi_phi_marketing +
                record.chi_phi_dien_nuoc +
                record.chi_phi_khac
            )
    
    @api.depends('doanh_thu', 'tong_chi_phi')
    def _compute_loi_nhuan(self):
        for record in self:
            record.loi_nhuan = record.doanh_thu - record.tong_chi_phi
    
    @api.depends('doanh_thu', 'loi_nhuan')
    def _compute_ty_le_loi_nhuan(self):
        for record in self:
            if record.doanh_thu > 0:
                record.ty_le_loi_nhuan = (record.loi_nhuan / record.doanh_thu) * 100
            else:
                record.ty_le_loi_nhuan = 0.0
    
    def _compute_bieu_do_du_lieu(self):
        """Tạo dữ liệu JSON cho biểu đồ doanh thu - chi phí"""
        for record in self:
            data = {
                'labels': ['Doanh thu', 'Tổng chi phí', 'Lợi nhuận'],
                'datasets': [{
                    'label': 'Triệu đồng',
                    'data': [
                        record.doanh_thu / 1000000,
                        record.tong_chi_phi / 1000000,
                        record.loi_nhuan / 1000000
                    ],
                    'backgroundColor': ['#28a745', '#dc3545', '#007bff']
                }]
            }
            record.bieu_do_du_lieu = json.dumps(data)
    
    def _compute_bieu_do_phan_bo_chi_phi(self):
        """Tạo dữ liệu JSON cho biểu đồ phân bổ chi phí"""
        for record in self:
            labels = ['Khấu hao', 'Lương', 'Văn phòng', 'Marketing', 'Điện nước', 'Khác']
            data = [
                record.chi_phi_khau_hao,
                record.chi_phi_luong,
                record.chi_phi_van_phong,
                record.chi_phi_marketing,
                record.chi_phi_dien_nuoc,
                record.chi_phi_khac
            ]
            
            # Lọc bỏ các mục có giá trị = 0
            filtered_data = []
            filtered_labels = []
            colors = ['#ff6384', '#36a2eb', '#ffce56', '#4bc0c0', '#9966ff', '#ff9f40']
            filtered_colors = []
            
            for i, value in enumerate(data):
                if value > 0:
                    filtered_data.append(value)
                    filtered_labels.append(labels[i])
                    filtered_colors.append(colors[i])
            
            chart_data = {
                'labels': filtered_labels,
                'datasets': [{
                    'data': filtered_data,
                    'backgroundColor': filtered_colors,
                    'hoverOffset': 4
                }]
            }
            record.bieu_do_phan_bo_chi_phi = json.dumps(chart_data)
    
    # ========== ACTION METHODS ==========
    def action_tinh_toan(self):
        """Phương thức xử lý khi click nút Tính toán"""
        for record in self:
            record.write({
                'trang_thai': 'in_progress',
                'nguoi_xu_ly_id': self.env.user.id
            })
            # Có thể thêm logic tính toán tự động ở đây
        return True
    
    def action_hoan_thanh(self):
        """Hoàn thành báo cáo"""
        for record in self:
            record.write({
                'trang_thai': 'completed',
                'ngay_hoan_thanh': fields.Datetime.now()
            })
        return True
    
    def action_quay_lai_nhap(self):
        """Quay lại trạng thái nháp"""
        for record in self:
            record.write({
                'trang_thai': 'draft'
            })
        return True
    
    def action_huy(self):
        """Hủy báo cáo"""
        for record in self:
            record.write({
                'trang_thai': 'cancelled'
            })
        return True
    
    def action_in_bao_cao(self):
        """In báo cáo"""
        return self.env.ref('quan_ly_tai_chinh.action_bao_cao_tai_chinh_pdf').report_action(self)
    
    # ========== WIZARD METHODS ==========
    def action_open_wizard_sao_chep(self):
        """Mở wizard sao chép báo cáo"""
        return {
            'name': 'Sao chép báo cáo',
            'type': 'ir.actions.act_window',
            'res_model': 'bao.cao.tai.chinh.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_bao_cao_id': self.id,
                'default_thang': self.thang,
                'default_nam': self.nam,
            }
        }