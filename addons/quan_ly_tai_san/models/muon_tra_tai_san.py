# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError

class MuonTraTaiSan(models.Model):
    """
    Model quản lý mượn trả tài sản
    Là nơi quản lý duyệt các đơn đăng ký mượn từ nhân viên
    Quy trình: Chờ duyệt -> Đã duyệt -> Đang mượn -> Đã trả
    """
    _name = 'muon_tra_tai_san'
    _description = 'Quản lý mượn trả tài sản'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "ma_phieu_muon_tra"
    _order = "create_date desc"
    _sql_constraints = [
        ("ma_phieu_muon_tra_unique", "unique(ma_phieu_muon_tra)", "Mã phiếu mượn trả đã tồn tại!"),
    ]

    # ============ THÔNG TIN PHIẾU ============
    ma_phieu_muon_tra = fields.Char(
        'Mã phiếu mượn trả', 
        required=True,
        readonly=True,
        copy=False,
        default='New',
        tracking=True
    )
    ten_phieu_muon_tra = fields.Char('Tên phiếu', required=True, tracking=True)
    
    # ============ LIÊN KẾT ĐƠN MƯỢN ============
    ma_don_muon_id = fields.Many2one(
        'don_muon_tai_san', 
        string='Đơn đăng ký mượn', 
        ondelete='restrict',
        tracking=True,
        readonly=True,
        help='Đơn đăng ký mượn từ nhân viên'
    )
    
    # ============ THÔNG TIN MƯỢN ============
    phong_ban_cho_muon_id = fields.Many2one(
        'phong_ban', 
        string='Phòng ban cho mượn', 
        required=True, 
        ondelete='restrict',
        tracking=True
    )
    nhan_vien_muon_id = fields.Many2one(
        'nhan_vien', 
        string='Nhân viên mượn', 
        required=True, 
        ondelete='restrict',
        tracking=True
    )
    
    thoi_gian_muon = fields.Datetime(
        'Thời gian mượn dự kiến', 
        required=True, 
        default=lambda self: fields.Datetime.now(),
        tracking=True
    )
    thoi_gian_muon_thuc_te = fields.Datetime(
        'Thời gian cho mượn thực tế',
        readonly=True,
        tracking=True,
        help='Thời điểm quản lý xác nhận giao tài sản'
    )
    thoi_gian_tra_du_kien = fields.Datetime(
        'Thời gian trả dự kiến', 
        required=True,
        tracking=True
    )
    thoi_gian_tra_thuc_te = fields.Datetime(
        'Thời gian trả thực tế',
        readonly=True,
        tracking=True
    )
    
    ly_do_muon = fields.Text('Lý do mượn', tracking=True)
    ghi_chu = fields.Text('Ghi chú quản lý', tracking=True)
    ly_do_tu_choi = fields.Text('Lý do từ chối')

    # ============ TRẠNG THÁI ============
    trang_thai = fields.Selection([
        ('cho_duyet', 'Chờ duyệt'),
        ('da_duyet', 'Đã duyệt'),
        ('dang_muon', 'Đang mượn'),
        ('da_tra', 'Đã trả'),
        ('tu_choi', 'Từ chối'),
        ('qua_han', 'Quá hạn')
    ], string='Trạng thái', required=True, default='cho_duyet', tracking=True)
    
    # ============ THÔNG TIN NGƯỜI XỬ LÝ ============
    nguoi_duyet_id = fields.Many2one(
        'res.users',
        string='Người duyệt',
        readonly=True,
        tracking=True
    )
    ngay_duyet = fields.Datetime('Ngày duyệt', readonly=True)
    
    nguoi_giao_id = fields.Many2one(
        'res.users',
        string='Người giao tài sản',
        readonly=True
    )
    
    nguoi_nhan_tra_id = fields.Many2one(
        'res.users',
        string='Người nhận trả',
        readonly=True
    )
    
    # ============ DANH SÁCH TÀI SẢN ============
    muon_tra_line_ids = fields.One2many(
        'muon_tra_tai_san_line', 
        'muon_tra_id', 
        string='Danh sách tài sản mượn'
    )
    
    ds_tai_san_chua_muon = fields.Many2many(
        'phan_bo_tai_san', 
        compute='_compute_ds_tai_san_chua_muon', 
        string="Tài sản có thể mượn thêm"
    )
    
    # ============ COMPUTED FIELDS ============
    tinh_trang = fields.Char(
        compute='_compute_tinh_trang',
        string='Tình trạng',
        store=False
    )
    
    so_tai_san = fields.Integer(
        compute='_compute_so_tai_san',
        string='Số tài sản'
    )
    
    # ============ COMPUTE METHODS ============
    @api.depends('muon_tra_line_ids')
    def _compute_so_tai_san(self):
        for record in self:
            record.so_tai_san = len(record.muon_tra_line_ids)
    
    @api.depends('phong_ban_cho_muon_id', 'muon_tra_line_ids')
    def _compute_ds_tai_san_chua_muon(self):
        for record in self:
            da_muon_ids = record.muon_tra_line_ids.mapped('phan_bo_tai_san_id').ids
            ds_tai_san = self.env['phan_bo_tai_san'].search([
                ('phong_ban_id', '=', record.phong_ban_cho_muon_id.id if record.phong_ban_cho_muon_id else False),
                ('id', 'not in', da_muon_ids),
                ('tinh_trang', '=', 'binh_thuong')  # Chỉ lấy tài sản đang sẵn sàng
            ])
            record.ds_tai_san_chua_muon = ds_tai_san
    
    @api.depends('trang_thai', 'thoi_gian_tra_du_kien')
    def _compute_tinh_trang(self):
        now = fields.Datetime.now()
        for record in self:
            if record.trang_thai == 'cho_duyet':
                record.tinh_trang = '⏳ Chờ duyệt'
            elif record.trang_thai == 'da_duyet':
                record.tinh_trang = '✔️ Đã duyệt - Chờ giao'
            elif record.trang_thai == 'tu_choi':
                record.tinh_trang = '❌ Đã từ chối'
            elif record.trang_thai == 'da_tra':
                record.tinh_trang = '✅ Đã hoàn trả'
            elif record.trang_thai == 'qua_han':
                record.tinh_trang = '⚠️ Quá hạn trả'
            elif record.trang_thai == 'dang_muon':
                if record.thoi_gian_tra_du_kien and now > record.thoi_gian_tra_du_kien:
                    record.tinh_trang = '⚠️ Quá hạn trả'
                else:
                    record.tinh_trang = '📦 Đang mượn'
            else:
                record.tinh_trang = 'Không xác định'
    
    # ============ CONSTRAINTS ============
    @api.constrains('thoi_gian_muon', 'thoi_gian_tra_du_kien')
    def _constrains_thoi_gian(self):
        for record in self:
            if record.thoi_gian_muon and record.thoi_gian_tra_du_kien:
                if record.thoi_gian_muon > record.thoi_gian_tra_du_kien:
                    raise ValidationError("Thời gian mượn phải trước thời gian trả!")
    
    # ============ CRUD METHODS ============
    @api.model
    def create(self, vals):
        # Tạo mã phiếu tự động
        if vals.get('ma_phieu_muon_tra', 'New') == 'New':
            vals['ma_phieu_muon_tra'] = self.env['ir.sequence'].next_by_code('muon_tra_tai_san') or 'MTTS-' + fields.Date.today().strftime('%Y%m%d%H%M')
        
        record = super(MuonTraTaiSan, self).create(vals)
        record.message_post(body=_('📋 Yêu cầu mượn tài sản đã được tạo, chờ duyệt.'))
        return record
    
    # ============ ACTION METHODS - DUYỆT ============
    def action_duyet_don(self):
        """Duyệt đơn mượn tài sản"""
        for record in self:
            if record.trang_thai != 'cho_duyet':
                raise UserError(_('Chỉ có thể duyệt đơn đang chờ duyệt!'))
            
            if not record.muon_tra_line_ids:
                raise UserError(_('Vui lòng thêm ít nhất một tài sản vào đơn mượn!'))
            
            record.write({
                'trang_thai': 'da_duyet',
                'nguoi_duyet_id': self.env.user.id,
                'ngay_duyet': fields.Datetime.now(),
            })
            
            # Cập nhật trạng thái đơn mượn gốc nếu có
            if record.ma_don_muon_id:
                record.ma_don_muon_id.write({'trang_thai': 'da_duyet'})
            
            record.message_post(body=_('✅ Đơn mượn đã được duyệt bởi %s.') % self.env.user.name)
    
    def action_tu_choi_don(self):
        """Mở wizard từ chối đơn mượn"""
        self.ensure_one()
        if self.trang_thai != 'cho_duyet':
            raise UserError(_('Chỉ có thể từ chối đơn đang chờ duyệt!'))
        
        return {
            'name': 'Lý do từ chối',
            'type': 'ir.actions.act_window',
            'res_model': 'muon_tra_tu_choi_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_muon_tra_id': self.id}
        }
    
    def action_xac_nhan_tu_choi(self, ly_do):
        """Xác nhận từ chối với lý do"""
        for record in self:
            record.write({
                'trang_thai': 'tu_choi',
                'nguoi_duyet_id': self.env.user.id,
                'ngay_duyet': fields.Datetime.now(),
                'ly_do_tu_choi': ly_do,
            })
            
            # Cập nhật trạng thái đơn mượn gốc nếu có
            if record.ma_don_muon_id:
                record.ma_don_muon_id.write({
                    'trang_thai': 'tu_choi',
                    'ly_do_tu_choi': ly_do,
                })
            
            record.message_post(body=_('❌ Đơn mượn đã bị từ chối. Lý do: %s') % ly_do)
    
    # ============ ACTION METHODS - CHO MƯỢN ============
    def action_xac_nhan_cho_muon(self):
        """Xác nhận đã giao tài sản cho người mượn"""
        for record in self:
            if record.trang_thai != 'da_duyet':
                raise UserError(_('Chỉ có thể xác nhận cho mượn đơn đã duyệt!'))
            
            now = fields.Datetime.now()
            record.write({
                'trang_thai': 'dang_muon',
                'thoi_gian_muon_thuc_te': now,
                'nguoi_giao_id': self.env.user.id,
            })
            
            # Cập nhật trạng thái các tài sản
            for line in record.muon_tra_line_ids:
                if line.phan_bo_tai_san_id:
                    line.phan_bo_tai_san_id.sudo().write({'tinh_trang': 'dang_muon'})
            
            # Cập nhật trạng thái đơn mượn gốc nếu có
            if record.ma_don_muon_id:
                record.ma_don_muon_id.write({'trang_thai': 'dang_muon'})
            
            record.message_post(body=_('📦 Tài sản đã được giao cho %s lúc %s bởi %s.') % (
                record.nhan_vien_muon_id.name, 
                now.strftime('%d/%m/%Y %H:%M'), 
                self.env.user.name
            ))
    
    # ============ ACTION METHODS - TRẢ ============
    def action_xac_nhan_tra(self):
        """Mở wizard xác nhận trả tài sản với tình trạng"""
        self.ensure_one()
        if self.trang_thai not in ['dang_muon', 'qua_han']:
            raise UserError(_('Chỉ có thể xác nhận trả cho đơn đang mượn!'))
        
        return {
            'name': 'Xác nhận trả tài sản',
            'type': 'ir.actions.act_window',
            'res_model': 'muon_tra_xac_nhan_tra_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_muon_tra_id': self.id}
        }
    
    def action_xac_nhan_tra_hoan_tat(self):
        """Hoàn tất xác nhận trả tài sản"""
        for record in self:
            now = fields.Datetime.now()
            record.write({
                'trang_thai': 'da_tra',
                'thoi_gian_tra_thuc_te': now,
                'nguoi_nhan_tra_id': self.env.user.id,
            })
            
            # Cập nhật trạng thái các tài sản về bình thường
            for line in record.muon_tra_line_ids:
                if line.phan_bo_tai_san_id:
                    # Cập nhật tình trạng dựa trên tình trạng khi trả
                    tinh_trang_moi = 'binh_thuong'
                    if line.tinh_trang_khi_tra == 'hu_hong':
                        tinh_trang_moi = 'hu_hong'
                    elif line.tinh_trang_khi_tra == 'mat':
                        tinh_trang_moi = 'mat'
                    
                    line.phan_bo_tai_san_id.sudo().write({'tinh_trang': tinh_trang_moi})
                    line.write({
                        'trang_thai_tra': 'da_tra' if line.tinh_trang_khi_tra in ['tot', 'binh_thuong'] else ('hong' if line.tinh_trang_khi_tra == 'hu_hong' else 'mat'),
                        'ngay_tra': now
                    })
            
            # Cập nhật trạng thái đơn mượn gốc nếu có
            if record.ma_don_muon_id:
                record.ma_don_muon_id.write({'trang_thai': 'da_tra'})
            
            record.message_post(body=_('✅ Tài sản đã được trả lúc %s. Người nhận: %s.') % (
                now.strftime('%d/%m/%Y %H:%M'), self.env.user.name))
    
    # ============ ACTION METHODS - GIA HẠN ============
    def action_gia_han(self):
        """Mở wizard gia hạn thời gian trả"""
        return {
            'name': 'Gia hạn thời gian trả',
            'type': 'ir.actions.act_window',
            'res_model': 'muon_tra_gia_han_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_muon_tra_id': self.id}
        }
    
    def action_view_don_muon(self):
        """Xem đơn mượn gốc"""
        self.ensure_one()
        if not self.ma_don_muon_id:
            raise UserError(_('Không có đơn mượn liên kết!'))
        return {
            'name': 'Đơn mượn tài sản',
            'type': 'ir.actions.act_window',
            'res_model': 'don_muon_tai_san',
            'view_mode': 'form',
            'res_id': self.ma_don_muon_id.id,
        }
    
    # ============ SCHEDULED ACTION ============
    @api.model
    def _cron_check_qua_han(self):
        """Kiểm tra và cập nhật các phiếu quá hạn"""
        now = fields.Datetime.now()
        qua_han_records = self.search([
            ('trang_thai', '=', 'dang_muon'),
            ('thoi_gian_tra_du_kien', '<', now)
        ])
        for record in qua_han_records:
            record.write({'trang_thai': 'qua_han'})
            record.message_post(body=_('⚠️ Phiếu mượn đã quá hạn trả!'))


class MuonTraTaiSanLine(models.Model):
    """Chi tiết từng tài sản trong phiếu mượn trả"""
    _name = 'muon_tra_tai_san_line'
    _description = 'Chi tiết tài sản mượn trả'
    
    muon_tra_id = fields.Many2one(
        'muon_tra_tai_san', 
        string='Phiếu mượn trả', 
        required=True, 
        ondelete='cascade'
    )
    phan_bo_tai_san_id = fields.Many2one(
        'phan_bo_tai_san', 
        string='Tài sản', 
        required=True,
        ondelete='restrict'
    )
    
    # Thông tin tài sản (từ phan_bo_tai_san)
    tai_san_id = fields.Many2one(
        related='phan_bo_tai_san_id.tai_san_id',
        string='Mã tài sản',
        store=True
    )
    ten_tai_san = fields.Char(
        related='phan_bo_tai_san_id.tai_san_id.ten_tai_san',
        string='Tên tài sản',
        store=True
    )
    
    ghi_chu = fields.Text('Ghi chú khi mượn')
    ghi_chu_tra = fields.Text('Ghi chú khi trả')
    
    trang_thai_tra = fields.Selection([
        ('chua_tra', 'Chưa trả'),
        ('da_tra', 'Đã trả'),
        ('hong', 'Bị hỏng'),
        ('mat', 'Bị mất')
    ], string='Trạng thái trả', default='chua_tra')
    
    ngay_tra = fields.Datetime('Ngày trả thực tế')
    
    tinh_trang_khi_tra = fields.Selection([
        ('tot', 'Tốt'),
        ('binh_thuong', 'Bình thường'),
        ('hu_hong', 'Hư hỏng'),
        ('mat', 'Mất')
    ], string='Tình trạng khi trả', default='tot')
