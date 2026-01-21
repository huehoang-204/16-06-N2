# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class DashboardTaiChinh(models.Model):
    """
    Dashboard tổng hợp tài chính - Hiển thị thống kê về:
    - Đề xuất mua tài sản
    - Khấu hao tài sản
    - Sổ cái và bút toán
    - Kế toán quản trị
    """
    _name = 'dashboard.tai.chinh'
    _description = 'Dashboard Tổng hợp Tài chính'

    name = fields.Char(string='Dashboard', default='Dashboard Tài chính', readonly=True)
    ngay_hien_tai = fields.Date(string='Ngày hiện tại', default=fields.Date.today, readonly=True)
    
    # ========== THỐNG KÊ PHÊ DUYỆT MUA TÀI SẢN ==========
    tong_phe_duyet = fields.Integer(
        string='Tổng đơn phê duyệt',
        compute='_compute_phe_duyet_stats',
        help='Tổng số đơn phê duyệt mua tài sản'
    )
    phe_duyet_cho_duyet = fields.Integer(
        string='Chờ phê duyệt',
        compute='_compute_phe_duyet_stats'
    )
    phe_duyet_da_duyet = fields.Integer(
        string='Đã phê duyệt',
        compute='_compute_phe_duyet_stats'
    )
    phe_duyet_hoan_thanh = fields.Integer(
        string='Hoàn thành',
        compute='_compute_phe_duyet_stats'  
    )
    phe_duyet_bi_tu_choi = fields.Integer(
        string='Bị từ chối',
        compute='_compute_phe_duyet_stats'
    )
    
    # Giá trị phê duyệt
    tong_gia_tri_phe_duyet = fields.Float(
        string='Tổng giá trị phê duyệt',
        compute='_compute_phe_duyet_stats'
    )
    gia_tri_cho_duyet = fields.Float(
        string='Giá trị chờ duyệt',
        compute='_compute_phe_duyet_stats'
    )
    gia_tri_da_duyet = fields.Float(
        string='Giá trị đã duyệt',
        compute='_compute_phe_duyet_stats'
    )
    
    # ========== THỐNG KÊ KHẤU HAO ==========
    # Tài sản
    tong_tai_san = fields.Integer(
        string='Tổng tài sản',
        compute='_compute_khau_hao_stats',
        help='Tổng số tài sản trong hệ thống'
    )
    tai_san_hoat_dong = fields.Integer(
        string='Tài sản hoạt động',
        compute='_compute_khau_hao_stats'
    )
    tai_san_dang_khau_hao = fields.Integer(
        string='Đang khấu hao',
        compute='_compute_khau_hao_stats'
    )
    tai_san_hoan_thanh_khau_hao = fields.Integer(
        string='Hoàn thành khấu hao',
        compute='_compute_khau_hao_stats'
    )
    
    # Giá trị tài sản
    tong_gia_tri_tai_san = fields.Float(
        string='Tổng giá trị tài sản',
        compute='_compute_khau_hao_stats'
    )
    tong_khau_hao_tich_luy = fields.Float(
        string='Tổng khấu hao tích lũy',
        compute='_compute_khau_hao_stats'
    )
    tong_gia_tri_con_lai = fields.Float(
        string='Tổng giá trị còn lại',
        compute='_compute_khau_hao_stats'
    )
    
    # Khấu hao theo thời gian
    khau_hao_thang_nay = fields.Float(
        string='Khấu hao tháng này',
        compute='_compute_khau_hao_stats'
    )
    khau_hao_quy_nay = fields.Float(
        string='Khấu hao quý này',
        compute='_compute_khau_hao_stats'
    )
    khau_hao_nam_nay = fields.Float(
        string='Khấu hao năm này',
        compute='_compute_khau_hao_stats'
    )
    
    # ========== BIỂU ĐỒ VÀ PHÂN TÍCH ==========
    depreciation_trend_ids = fields.One2many(
        'dashboard.depreciation.trend', 
        'dashboard_id', 
        string='Xu hướng khấu hao',
        help='Biểu đồ xu hướng khấu hao theo tháng'
    )
    purchase_trend_ids = fields.One2many(
        'dashboard.purchase.trend', 
        'dashboard_id', 
        string='Xu hướng mua sắm',
        help='Biểu đồ xu hướng mua sắm theo tháng'
    )
    department_distribution_ids = fields.One2many(
        'dashboard.department.distribution', 
        'dashboard_id', 
        string='Phân bổ theo phòng ban',
        help='Phân bổ tài sản và đề xuất theo phòng ban'
    )
    
    # ========== THỐNG KÊ SỔ CÁI ==========
    tong_but_toan = fields.Integer(
        string='Tổng bút toán',
        compute='_compute_but_toan_stats'
    )
    but_toan_nhap = fields.Integer(
        string='Bút toán nháp',
        compute='_compute_but_toan_stats'
    )
    but_toan_da_ghi = fields.Integer(
        string='Bút toán đã ghi',
        compute='_compute_but_toan_stats'
    )
    
    tong_gia_tri_but_toan = fields.Float(
        string='Tổng giá trị bút toán',
        compute='_compute_but_toan_stats'
    )
    
    # ========== THỐNG KÊ KẾ TOÁN QUẢN TRỊ ==========
    tong_chi_phi = fields.Float(
        string='Tổng chi phí',
        compute='_compute_ke_toan_quan_tri_stats'
    )
    chi_phi_thang_nay = fields.Float(
        string='Chi phí tháng này',
        compute='_compute_ke_toan_quan_tri_stats'
    )
    
    # ========== COMPUTE METHODS ==========
    
    def _compute_phe_duyet_stats(self):
        """Tính toán thống kê phê duyệt mua tài sản"""
        for record in self:
            phe_duyet_obj = self.env['phe_duyet_mua_tai_san']
            
            # Đếm theo trạng thái
            record.tong_phe_duyet = phe_duyet_obj.search_count([])
            record.phe_duyet_cho_duyet = phe_duyet_obj.search_count([('state', '=', 'draft')])
            record.phe_duyet_da_duyet = phe_duyet_obj.search_count([('state', '=', 'approved')])
            record.phe_duyet_hoan_thanh = phe_duyet_obj.search_count([('state', '=', 'done')])
            record.phe_duyet_bi_tu_choi = phe_duyet_obj.search_count([('state', '=', 'rejected')])
            
            # Tính tổng giá trị
            all_phe_duyet = phe_duyet_obj.search([])
            record.tong_gia_tri_phe_duyet = sum(all_phe_duyet.mapped('tong_gia_tri'))
            
            cho_duyet = phe_duyet_obj.search([('state', '=', 'draft')])
            record.gia_tri_cho_duyet = sum(cho_duyet.mapped('tong_gia_tri'))
            
            da_duyet = phe_duyet_obj.search([('state', 'in', ['approved', 'done'])])
            record.gia_tri_da_duyet = sum(da_duyet.mapped('tong_gia_tri'))
    
    def _compute_khau_hao_stats(self):
        """Tính toán thống kê khấu hao"""
        for record in self:
            tai_san_obj = self.env['tai_san']
            khau_hao_obj = self.env['khau_hao_tai_san']
            
            # Đếm tài sản
            record.tong_tai_san = tai_san_obj.search_count([])
            record.tai_san_hoat_dong = tai_san_obj.search_count([('trang_thai_thanh_ly', '=', 'da_phan_bo')])
            
            # Đếm khấu hao
            record.tai_san_dang_khau_hao = khau_hao_obj.search_count([('trang_thai', '=', 'dang_khau_hao')])
            record.tai_san_hoan_thanh_khau_hao = khau_hao_obj.search_count([('trang_thai', '=', 'hoan_thanh')])
            
            # Tính giá trị
            all_tai_san = tai_san_obj.search([])
            record.tong_gia_tri_tai_san = sum(all_tai_san.mapped('gia_tri_ban_dau'))
            record.tong_gia_tri_con_lai = sum(all_tai_san.mapped('gia_tri_hien_tai'))
            record.tong_khau_hao_tich_luy = record.tong_gia_tri_tai_san - record.tong_gia_tri_con_lai
            
            # Khấu hao theo thời gian
            today = fields.Date.today()
            
            # Tháng này
            thang_dau = today.replace(day=1)
            thang_cuoi = (thang_dau + relativedelta(months=1)) - relativedelta(days=1)
            
            khau_hao_thang = khau_hao_obj.search([
                ('ngay_bat_dau', '<=', thang_cuoi),
                ('trang_thai', '=', 'dang_khau_hao')
            ])
            record.khau_hao_thang_nay = sum(khau_hao_thang.mapped('gia_tri_khau_hao_hang_nam')) / 12
            
            # Quý này
            quy = (today.month - 1) // 3
            quy_dau = today.replace(month=quy*3 + 1, day=1)
            quy_cuoi = (quy_dau + relativedelta(months=3)) - relativedelta(days=1)
            
            record.khau_hao_quy_nay = record.khau_hao_thang_nay * 3
            
            # Năm này
            record.khau_hao_nam_nay = sum(khau_hao_obj.search([
                ('ngay_bat_dau', '<=', today),
                ('trang_thai', '=', 'dang_khau_hao')
            ]).mapped('gia_tri_khau_hao_hang_nam'))
    
    def _compute_but_toan_stats(self):
        """Tính toán thống kê bút toán"""
        for record in self:
            but_toan_obj = self.env['account.move']
            record.tong_but_toan = but_toan_obj.search_count([])
            record.but_toan_da_ghi = but_toan_obj.search_count([('state', '=', 'posted')])
            record.but_toan_nhap = but_toan_obj.search_count([('state', '=', 'draft')])
            
            all_but_toan = but_toan_obj.search([])
            record.tong_gia_tri_but_toan = sum(all_but_toan.mapped('amount_total')) if all_but_toan else 0
    
    def _compute_ke_toan_quan_tri_stats(self):
        """Tính toán thống kê kế toán quản trị"""
        for record in self:
            tai_khoan_obj = self.env['tai_khoan_quan_tri']
            all_tai_khoan = tai_khoan_obj.search([])
            record.tong_chi_phi = sum(all_tai_khoan.mapped('so_tien')) if all_tai_khoan else 0
            
            # Chi phí tháng này
            today = date.today()
            month_start = today.replace(day=1)
            chi_phi_thang = tai_khoan_obj.search([
                ('ngay_ghi_nhan', '>=', month_start)
            ])
            record.chi_phi_thang_nay = sum(chi_phi_thang.mapped('so_tien')) if chi_phi_thang else 0
    
    # ========== ACTION METHODS ==========
    
    def action_view_phe_duyet(self):
        """Xem danh sách phê duyệt"""
        return {
            'name': 'Phê duyệt mua tài sản',
            'type': 'ir.actions.act_window',
            'res_model': 'phe_duyet_mua_tai_san',
            'view_mode': 'tree,form',
            'context': {'search_default_draft': 1}
        }
    
    def action_view_khau_hao(self):
        """Xem danh sách khấu hao"""
        return {
            'name': 'Khấu hao tài sản',
            'type': 'ir.actions.act_window',
            'res_model': 'khau_hao_tai_san',
            'view_mode': 'tree,form',
            'context': {'search_default_dang_khau_hao': 1}
        }
    
    def action_view_tai_san(self):
        """Xem danh sách tài sản"""
        return {
            'name': 'Tài sản',
            'type': 'ir.actions.act_window',
            'res_model': 'tai_san',
            'view_mode': 'tree,form',
        }
    
    def action_view_but_toan(self):
        """Xem danh sách bút toán"""
        phe_duyet_ids = self.env['phe_duyet_mua_tai_san'].search([])
        but_toan_ids = phe_duyet_ids.mapped('but_toan_id').ids
        
        return {
            'name': 'Bút toán tài sản',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', but_toan_ids)]
        }
    
    def action_refresh(self):
        """Làm mới dashboard - Version đơn giản"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thành công',
                'message': 'Dữ liệu dashboard đã được làm mới',
                'type': 'success',
                'sticky': False,
            }
        }
    
    def _compute_depreciation_trend(self):
        """Tính toán xu hướng khấu hao 12 tháng gần nhất"""
        for record in self:
            # Xóa dữ liệu cũ
            record.depreciation_trend_ids.unlink()
            
            # Tính toán 12 tháng gần nhất
            trends = []
            today = date.today()
            
            for i in range(11, -1, -1):
                month_date = today - relativedelta(months=i)
                month_str = month_date.strftime('%Y-%m')
                
                # Đơn giản: lấy khấu hao đang hoạt động trong 12 tháng
                khau_hao_records = self.env['khau_hao_tai_san'].search([
                    ('trang_thai', '=', 'dang_khau_hao')
                ])
                
                total_amount = sum(khau_hao_records.mapped('gia_tri_khau_hao_hang_nam'))
                count = len(khau_hao_records)
                
                trends.append((0, 0, {
                    'month': month_str,
                    'amount': total_amount,
                    'count': count
                }))
            
            record.depreciation_trend_ids = trends
    
    def _compute_purchase_trend(self):
        """Tính toán xu hướng mua sắm 12 tháng gần nhất"""
        for record in self:
            # Xóa dữ liệu cũ
            record.purchase_trend_ids.unlink()
            
            trends = []
            today = date.today()
            
            for i in range(11, -1, -1):
                month_date = today - relativedelta(months=i)
                month_str = month_date.strftime('%Y-%m')
                
                # Đơn giản: lấy tất cả phê duyệt
                all_phe_duyet = self.env['phe_duyet_mua_tai_san'].search([])
                
                # Đề xuất đã được phê duyệt
                approved_phe_duyet = all_phe_duyet.filtered(lambda p: p.trang_thai in ['approved', 'done'])
                
                trends.append((0, 0, {
                    'month': month_str,
                    'amount': sum(all_phe_duyet.mapped('tong_gia_tri')) if all_phe_duyet else 0,
                    'count': len(all_phe_duyet),
                    'amount_approved': sum(approved_phe_duyet.mapped('tong_gia_tri')) if approved_phe_duyet else 0,
                    'count_approved': len(approved_phe_duyet)
                }))
            
            record.purchase_trend_ids = trends
    
    def _compute_department_distribution(self):
        """Tính toán phân bổ theo phòng ban"""
        for record in self:
            # Xóa dữ liệu cũ
            record.department_distribution_ids.unlink()
            
            distributions = []
            departments = self.env['hr.department'].search([])
            
            for dept in departments:
                # Tài sản của phòng ban
                tai_san_records = self.env['tai_san'].search([
                    ('phong_ban_id', '=', dept.id),
                    ('trang_thai', '!=', 'thanh_ly')
                ])
                
                # Đề xuất của phòng ban
                de_xuat_records = self.env['phe_duyet_mua_tai_san'].search([
                    ('phong_ban_id', '=', dept.id)
                ])
                
                approved_de_xuat = de_xuat_records.filtered(lambda d: d.trang_thai == 'approved')
                
                if tai_san_records or de_xuat_records:
                    distributions.append((0, 0, {
                        'department_id': dept.id,
                        'tai_san_count': len(tai_san_records),
                        'tai_san_value': sum(tai_san_records.mapped('nguyen_gia')),
                        'de_xuat_count': len(de_xuat_records),
                        'de_xuat_value': sum(de_xuat_records.mapped('tong_gia_tri')),
                        'approved_count': len(approved_de_xuat),
                        'approved_value': sum(approved_de_xuat.mapped('tong_gia_tri'))
                    }))
            
            record.department_distribution_ids = distributions


# ========== MODELS PHỤ TRỢ CHO BIỂU ĐỒ ==========

class DashboardDepreciationTrend(models.Model):
    """Model lưu xu hướng khấu hao theo tháng"""
    _name = 'dashboard.depreciation.trend'
    _description = 'Xu hướng khấu hao theo tháng'
    _order = 'month'

    dashboard_id = fields.Many2one('dashboard.tai.chinh', string='Dashboard', ondelete='cascade', required=True)
    month = fields.Char(string='Tháng', required=True, help='Tháng theo định dạng YYYY-MM')
    amount = fields.Float(string='Số tiền khấu hao', help='Tổng giá trị khấu hao trong tháng')
    count = fields.Integer(string='Số lượng', help='Số lượng tài sản được khấu hao')
    company_id = fields.Many2one('res.company', string='Công ty', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Tiền tệ', related='company_id.currency_id', readonly=True)


class DashboardPurchaseTrend(models.Model):
    """Model lưu xu hướng mua sắm theo tháng"""
    _name = 'dashboard.purchase.trend'
    _description = 'Xu hướng mua sắm theo tháng'
    _order = 'month'

    dashboard_id = fields.Many2one('dashboard.tai.chinh', string='Dashboard', ondelete='cascade', required=True)
    month = fields.Char(string='Tháng', required=True, help='Tháng theo định dạng YYYY-MM')
    amount = fields.Float(string='Giá trị mua sắm', help='Tổng giá trị đề xuất mua tài sản')
    count = fields.Integer(string='Số lượng đề xuất', help='Số lượng đề xuất được phê duyệt')
    amount_approved = fields.Float(string='Giá trị đã duyệt', help='Giá trị các đề xuất đã được phê duyệt')
    count_approved = fields.Integer(string='Số lượng đã duyệt', help='Số đề xuất đã được phê duyệt')
    company_id = fields.Many2one('res.company', string='Công ty', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Tiền tệ', related='company_id.currency_id', readonly=True)


class DashboardDepartmentDistribution(models.Model):
    """Model lưu phân bổ tài sản và đề xuất theo phòng ban"""
    _name = 'dashboard.department.distribution'
    _description = 'Phân bổ theo phòng ban'
    _order = 'department_id'

    dashboard_id = fields.Many2one('dashboard.tai.chinh', string='Dashboard', ondelete='cascade', required=True)
    department_id = fields.Many2one('hr.department', string='Phòng ban', required=True)
    tai_san_count = fields.Integer(string='Số tài sản', help='Số lượng tài sản đang quản lý')
    tai_san_value = fields.Float(string='Giá trị tài sản', help='Tổng giá trị tài sản hiện tại')
    de_xuat_count = fields.Integer(string='Số đề xuất', help='Số lượng đề xuất mua tài sản')
    de_xuat_value = fields.Float(string='Giá trị đề xuất', help='Tổng giá trị đề xuất')
    approved_count = fields.Integer(string='Số đề xuất đã duyệt', help='Số đề xuất đã được phê duyệt')
    approved_value = fields.Float(string='Giá trị đã duyệt', help='Giá trị đề xuất đã được phê duyệt')
    company_id = fields.Many2one('res.company', string='Công ty', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Tiền tệ', related='company_id.currency_id', readonly=True)
