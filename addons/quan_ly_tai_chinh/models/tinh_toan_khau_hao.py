# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class TinhToanKhauHaoTuDong(models.Model):
    """
    Model quản lý tính toán khấu hao tự động hàng tháng
    Tự động tạo các bút toán khấu hao định kỳ
    """
    _name = 'tinh.toan.khau.hao'
    _description = 'Tính toán khấu hao tự động'
    _rec_name = 'thang_nam'
    _order = 'thang_nam desc'
    
    # ========== THÔNG TIN THÁNG ==========
    thang_nam = fields.Char(
        string='Tháng/Năm',
        required=True,
        readonly=True,
        help='Tháng và năm tính khấu hao (MM/YYYY)'
    )
    
    thang = fields.Integer(string='Tháng', required=True, readonly=True)
    nam = fields.Integer(string='Năm', required=True, readonly=True)
    
    ngay_tinh = fields.Date(
        string='Ngày tính',
        default=fields.Date.today,
        required=True,
        readonly=True
    )
    
    # ========== TRẠNG THÁI ==========
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('calculated', 'Đã tính toán'),
        ('posted', 'Đã ghi sổ'),
        ('cancelled', 'Đã hủy')
    ], string='Trạng thái', default='draft', required=True, tracking=True)
    
    # ========== CHI TIẾT KHẤU HAO ==========
    line_ids = fields.One2many(
        'tinh.toan.khau.hao.line',
        'tinh_toan_id',
        string='Chi tiết khấu hao'
    )
    
    # ========== TỔNG HỢP ==========
    tong_so_tai_san = fields.Integer(
        string='Tổng số tài sản',
        compute='_compute_tong_hop',
        store=True
    )
    
    tong_khau_hao_thang = fields.Float(
        string='Tổng khấu hao tháng',
        compute='_compute_tong_hop',
        store=True
    )
    
    # ========== BÚT TOÁN ==========
    but_toan_ids = fields.One2many(
        'account.move',
        'tinh_toan_khau_hao_id',
        string='Bút toán khấu hao',
        readonly=True
    )
    
    but_toan_count = fields.Integer(
        string='Số bút toán',
        compute='_compute_but_toan_count'
    )
    
    # ========== GHI CHÚ ==========
    ghi_chu = fields.Text(string='Ghi chú')
    
    # ========== COMPUTE METHODS ==========
    
    @api.depends('line_ids.so_tien_khau_hao')
    def _compute_tong_hop(self):
        for record in self:
            record.tong_so_tai_san = len(record.line_ids)
            record.tong_khau_hao_thang = sum(record.line_ids.mapped('so_tien_khau_hao'))
    
    @api.depends('but_toan_ids')
    def _compute_but_toan_count(self):
        for record in self:
            record.but_toan_count = len(record.but_toan_ids)
    
    # ========== CRUD METHODS ==========
    
    @api.model
    def create(self, vals):
        """Tự động tạo mã tháng/năm"""
        if vals.get('thang') and vals.get('nam'):
            vals['thang_nam'] = f"{vals['thang']:02d}/{vals['nam']}"
        return super(TinhToanKhauHaoTuDong, self).create(vals)
    
    # ========== ACTION METHODS ==========
    
    def action_calculate(self):
        """Tính toán khấu hao tự động"""
        self.ensure_one()
        
        if self.state != 'draft':
            raise UserError(_('Chỉ có thể tính toán ở trạng thái nháp.'))
        
        # Xóa các dòng cũ
        self.line_ids.unlink()
        
        # Lấy tất cả khấu hao đang hoạt động
        khau_hao_obj = self.env['khau_hao_tai_san']
        khau_hao_list = khau_hao_obj.search([
            ('trang_thai', '=', 'dang_khau_hao'),
            ('ngay_bat_dau', '<=', self.ngay_tinh)
        ])
        
        line_vals = []
        for khau_hao in khau_hao_list:
            # Tính số tháng đã khấu hao
            so_thang = self._tinh_so_thang_khau_hao(khau_hao.ngay_bat_dau, self.ngay_tinh)
            
            # Kiểm tra đã hết thời gian khấu hao chưa
            if so_thang <= khau_hao.so_nam_khau_hao * 12:
                # Tính khấu hao tháng này
                khau_hao_thang = khau_hao.gia_tri_khau_hao_hang_nam / 12
                
                line_vals.append({
                    'tinh_toan_id': self.id,
                    'khau_hao_tai_san_id': khau_hao.id,
                    'tai_san_id': khau_hao.tai_san_id.id,
                    'gia_tri_ban_dau': khau_hao.tai_san_id.gia_tri_ban_dau if khau_hao.tai_san_id else 0,
                    'ty_le_khau_hao': khau_hao.ty_le_khau_hao if hasattr(khau_hao, 'ty_le_khau_hao') else 0,
                    'so_tien_khau_hao': khau_hao_thang,
                    'so_thang_da_khau_hao': so_thang,
                })
        
        # Tạo các dòng
        self.env['tinh.toan.khau.hao.line'].create(line_vals)
        
        # Cập nhật trạng thái
        self.state = 'calculated'
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Thành công'),
                'message': f'Đã tính toán khấu hao cho {len(line_vals)} tài sản.',
                'type': 'success',
                'sticky': False,
            }
        }
    
    def action_create_journal_entries(self):
        """Tạo bút toán khấu hao"""
        self.ensure_one()
        
        if self.state != 'calculated':
            raise UserError(_('Vui lòng tính toán khấu hao trước khi ghi sổ.'))
        
        if self.tong_khau_hao_thang <= 0:
            raise UserError(_('Không có giá trị khấu hao để ghi sổ.'))
        
        # Tìm sổ nhật ký
        journal = self.env['account.journal'].search([('type', '=', 'general')], limit=1)
        if not journal:
            raise UserError(_('Không tìm thấy sổ nhật ký chung.'))
        
        # Tìm tài khoản chi phí khấu hao (6271)
        tk_chi_phi_kh = self.env['account.account'].search([
            ('code', '=like', '6271%'),
            ('deprecated', '=', False)
        ], limit=1)
        
        # Tìm tài khoản khấu hao lũy kế (2141)
        tk_khau_hao_lk = self.env['account.account'].search([
            ('code', '=like', '2141%'),
            ('deprecated', '=', False)
        ], limit=1)
        
        if not tk_chi_phi_kh or not tk_khau_hao_lk:
            raise UserError(_(
                'Không tìm thấy tài khoản khấu hao.\n'
                'Vui lòng thiết lập:\n'
                '- TK 6271: Chi phí khấu hao TSCĐ\n'
                '- TK 2141: Hao mòn TSCĐ hữu hình'
            ))
        
        # Tạo bút toán tổng hợp
        move_vals = {
            'journal_id': journal.id,
            'date': self.ngay_tinh,
            'ref': f'Khấu hao tháng {self.thang_nam}',
            'tinh_toan_khau_hao_id': self.id,
            'line_ids': [
                # Nợ TK Chi phí khấu hao
                (0, 0, {
                    'name': f'Chi phí khấu hao TSCĐ tháng {self.thang_nam}',
                    'account_id': tk_chi_phi_kh.id,
                    'debit': self.tong_khau_hao_thang,
                    'credit': 0,
                }),
                # Có TK Hao mòn lũy kế
                (0, 0, {
                    'name': f'Hao mòn lũy kế TSCĐ tháng {self.thang_nam}',
                    'account_id': tk_khau_hao_lk.id,
                    'debit': 0,
                    'credit': self.tong_khau_hao_thang,
                }),
            ]
        }
        
        move = self.env['account.move'].create(move_vals)
        move.action_post()
        
        # Cập nhật trạng thái
        self.state = 'posted'
        
        # Cập nhật lịch khấu hao đã ghi nhận
        for line in self.line_ids:
            if line.khau_hao_tai_san_id:
                # Cập nhật ngày khấu hao cuối
                line.khau_hao_tai_san_id.write({
                    'last_depreciation_date': self.ngay_tinh
                })
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Thành công'),
                'message': f'Đã tạo bút toán khấu hao: {move.name}',
                'type': 'success',
                'sticky': False,
            }
        }
    
    def action_cancel(self):
        """Hủy tính toán"""
        self.ensure_one()
        
        if self.state == 'posted':
            raise UserError(_('Không thể hủy tính toán đã ghi sổ. Vui lòng hủy bút toán trước.'))
        
        self.state = 'cancelled'
    
    def action_reset_to_draft(self):
        """Đưa về nháp"""
        self.ensure_one()
        
        if self.state == 'posted':
            raise UserError(_('Không thể đưa về nháp khi đã ghi sổ.'))
        
        self.line_ids.unlink()
        self.state = 'draft'
    
    def action_view_journal_entries(self):
        """Xem bút toán"""
        self.ensure_one()
        
        return {
            'name': _('Bút toán khấu hao'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.but_toan_ids.ids)],
            'context': {'create': False}
        }
    
    # ========== HELPER METHODS ==========
    
    def _tinh_so_thang_khau_hao(self, ngay_bat_dau, ngay_hien_tai):
        """Tính số tháng đã khấu hao"""
        if not ngay_bat_dau:
            return 0
        
        delta = relativedelta(ngay_hien_tai, ngay_bat_dau)
        return delta.years * 12 + delta.months + 1
    
    # ========== CRON JOB ==========
    
    @api.model
    def cron_tinh_khau_hao_hang_thang(self):
        """
        Tự động tính khấu hao hàng tháng
        Chạy vào ngày cuối tháng
        """
        today = fields.Date.today()
        
        # Kiểm tra đã có bản ghi tháng này chưa
        existing = self.search([
            ('thang', '=', today.month),
            ('nam', '=', today.year)
        ])
        
        if existing:
            _logger.info(f'Đã tồn tại bản ghi tính khấu hao tháng {today.month}/{today.year}')
            return
        
        # Tạo bản ghi mới
        record = self.create({
            'thang': today.month,
            'nam': today.year,
            'ngay_tinh': today,
        })
        
        # Tự động tính toán
        record.action_calculate()
        
        # Tự động ghi sổ (tùy chọn)
        # record.action_create_journal_entries()
        
        _logger.info(f'Đã tạo và tính toán khấu hao tháng {today.month}/{today.year}')


class TinhToanKhauHaoLine(models.Model):
    """Chi tiết tính toán khấu hao từng tài sản"""
    _name = 'tinh.toan.khau.hao.line'
    _description = 'Chi tiết tính toán khấu hao'
    _order = 'tai_san_id'
    
    tinh_toan_id = fields.Many2one(
        'tinh.toan.khau.hao',
        string='Tính toán khấu hao',
        required=True,
        ondelete='cascade'
    )
    
    khau_hao_tai_san_id = fields.Many2one(
        'khau_hao_tai_san',
        string='Khấu hao tài sản',
        required=True
    )
    
    tai_san_id = fields.Many2one(
        'tai_san',
        string='Tài sản',
        required=True
    )
    
    gia_tri_ban_dau = fields.Float(
        string='Giá trị ban đầu',
        readonly=True
    )
    
    ty_le_khau_hao = fields.Float(
        string='Tỷ lệ khấu hao (%)',
        readonly=True
    )
    
    so_tien_khau_hao = fields.Float(
        string='Số tiền khấu hao',
        required=True
    )
    
    so_thang_da_khau_hao = fields.Integer(
        string='Số tháng đã khấu hao',
        readonly=True
    )
    
    ghi_chu = fields.Text(string='Ghi chú')


# Thêm field vào account.move để liên kết
class AccountMove(models.Model):
    _inherit = 'account.move'
    
    tinh_toan_khau_hao_id = fields.Many2one(
        'tinh.toan.khau.hao',
        string='Tính toán khấu hao',
        readonly=True,
        ondelete='restrict'
    )


# Thêm field vào khau_hao_tai_san
class KhauHaoTaiSan(models.Model):
    _inherit = 'khau_hao_tai_san'
    
    last_depreciation_date = fields.Date(
        string='Ngày khấu hao cuối',
        help='Ngày khấu hao gần nhất'
    )
