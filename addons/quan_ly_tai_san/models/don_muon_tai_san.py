# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError

class DonMuonTaiSan(models.Model):
    _name = 'don_muon_tai_san'
    _description = 'Bảng chứa thông tin Đơn mượn tài sản'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "custom_rec_name"
    _order = "create_date desc"
    _sql_constraints = [
        ("ma_don_muon_unique", "unique(ma_don_muon)", "Mã đơn mượn đã tồn tại"),
    ]

    # ============ THÔNG TIN CƠ BẢN ============
    ma_don_muon = fields.Char(
        "Mã đơn mượn", 
        required=True, 
        default='New',
        readonly=True,
        copy=False,
        tracking=True
    )
    ten_don_muon = fields.Char('Tên đơn mượn', required=True, tracking=True)
    
    # ============ THÔNG TIN MƯỢN ============
    phong_ban_cho_muon_id = fields.Many2one(
        'phong_ban', 
        string='Phòng ban cho mượn', 
        required=True, 
        ondelete='restrict',
        tracking=True
    )
    thoi_gian_muon = fields.Datetime(
        'Thời gian mượn', 
        required=True, 
        default=lambda self: fields.Datetime.now(),
        tracking=True
    )
    thoi_gian_tra = fields.Datetime(
        'Thời gian trả dự kiến', 
        required=True,
        tracking=True
    )
    nhan_vien_muon_id = fields.Many2one(
        'nhan_vien', 
        string='Nhân viên mượn', 
        required=True, 
        ondelete='restrict',
        tracking=True
    )
    
    ly_do = fields.Text('Lý do mượn', required=True)
    ghi_chu = fields.Text('Ghi chú')
    
    # ============ DANH SÁCH TÀI SẢN ============
    don_muon_tai_san_ids = fields.One2many(
        'don_muon_tai_san_line', 
        'don_muon_id', 
        string='Danh sách tài sản mượn'
    )
    ds_tai_san_chua_muon = fields.Many2many(
        'phan_bo_tai_san', 
        compute='_compute_ds_tai_san_chua_muon', 
        string="Tài sản có thể mượn"
    )
    
    # ============ TRẠNG THÁI ============
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('cho_duyet', 'Chờ duyệt'),
        ('da_duyet', 'Đã duyệt'),
        ('dang_muon', 'Đang mượn'),
        ('da_tra', 'Đã trả'),
        ('tu_choi', 'Từ chối'),
        ('huy', 'Đã hủy')
    ], string='Trạng thái', required=True, default='nhap', tracking=True)
    
    # ============ THÔNG TIN DUYỆT ============
    nguoi_duyet_id = fields.Many2one(
        'res.users',
        string='Người duyệt',
        readonly=True,
        tracking=True
    )
    ngay_duyet = fields.Datetime('Ngày duyệt', readonly=True)
    ly_do_tu_choi = fields.Text('Lý do từ chối')
    
    # ============ THÔNG TIN TRẢ ============
    ngay_tra_thuc_te = fields.Datetime('Ngày trả thực tế', readonly=True)
    nguoi_xac_nhan_tra_id = fields.Many2one(
        'res.users',
        string='Người xác nhận trả',
        readonly=True
    )
    
    # ============ COMPUTED FIELDS ============
    custom_rec_name = fields.Char(
        compute='_compute_custom_rec_name', 
        string='Tên hiển thị',
        store=True
    )
    
    so_tai_san = fields.Integer(
        compute='_compute_so_tai_san',
        string='Số tài sản mượn'
    )
    
    tinh_trang = fields.Char(
        compute='_compute_tinh_trang',
        string='Tình trạng'
    )
    
    # ============ COMPUTE METHODS ============
    @api.depends('ma_don_muon', 'ten_don_muon')
    def _compute_custom_rec_name(self):
        for record in self:
            if record.ma_don_muon and record.ten_don_muon:
                record.custom_rec_name = f"{record.ma_don_muon} - {record.ten_don_muon}"
            else:
                record.custom_rec_name = record.ma_don_muon or 'New'
    
    @api.depends('don_muon_tai_san_ids')
    def _compute_so_tai_san(self):
        for record in self:
            record.so_tai_san = len(record.don_muon_tai_san_ids)

    @api.depends('phong_ban_cho_muon_id', 'don_muon_tai_san_ids')
    def _compute_ds_tai_san_chua_muon(self):
        for record in self:
            da_muon_ids = record.don_muon_tai_san_ids.mapped('phan_bo_tai_san_id').ids
            # Tìm tài sản thuộc phòng ban cho mượn và chưa được mượn
            ds_tai_san = self.env['phan_bo_tai_san'].search([
                ('phong_ban_id', '=', record.phong_ban_cho_muon_id.id if record.phong_ban_cho_muon_id else False),
                ('id', 'not in', da_muon_ids)
            ])
            record.ds_tai_san_chua_muon = ds_tai_san
    
    @api.depends('trang_thai', 'thoi_gian_muon', 'thoi_gian_tra')
    def _compute_tinh_trang(self):
        for record in self:
            if record.trang_thai == 'da_tra':
                record.tinh_trang = '✅ Đã hoàn trả'
            elif record.trang_thai == 'dang_muon':
                now = fields.Datetime.now()
                if record.thoi_gian_tra and now > record.thoi_gian_tra:
                    record.tinh_trang = '⚠️ Quá hạn trả'
                else:
                    record.tinh_trang = '📦 Đang mượn'
            elif record.trang_thai == 'da_duyet':
                record.tinh_trang = '✔️ Đã duyệt - Chờ nhận'
            elif record.trang_thai == 'cho_duyet':
                record.tinh_trang = '⏳ Đang chờ duyệt'
            elif record.trang_thai == 'tu_choi':
                record.tinh_trang = '❌ Đã từ chối'
            elif record.trang_thai == 'huy':
                record.tinh_trang = '🚫 Đã hủy'
            else:
                record.tinh_trang = '📝 Nháp'
    
    # ============ CONSTRAINTS ============
    @api.constrains('thoi_gian_muon', 'thoi_gian_tra')
    def _constrains_thoi_gian(self):
        for record in self:
            if record.thoi_gian_muon and record.thoi_gian_tra:
                if record.thoi_gian_muon > record.thoi_gian_tra:
                    raise ValidationError("Thời gian mượn phải trước thời gian trả dự kiến!")
    
    @api.constrains('don_muon_tai_san_ids')
    def _constrains_don_muon_tai_san_ids(self):
        for record in self:
            if record.trang_thai not in ['nhap', 'cho_duyet'] and not record.don_muon_tai_san_ids:
                raise ValidationError("Đơn mượn phải có ít nhất một tài sản!")
    
    # ============ CRUD METHODS ============
    @api.model
    def create(self, vals):
        if vals.get('ma_don_muon', 'New') == 'New':
            vals['ma_don_muon'] = self.env['ir.sequence'].next_by_code('don_muon_tai_san') or 'DMT-' + fields.Date.today().strftime('%Y%m%d')
        return super(DonMuonTaiSan, self).create(vals)
    
    # ============ ACTION METHODS ============
    def action_gui_duyet(self):
        """Gửi đơn để duyệt - Tự động tạo phiếu trong Quản lý mượn trả"""
        for record in self:
            # Kiểm tra xem record đã được lưu chưa
            if isinstance(record.id, models.NewId):
                raise UserError(_('Vui lòng lưu đơn mượn trước khi gửi duyệt!'))
            
            if record.trang_thai != 'nhap':
                raise UserError(_('Chỉ có thể gửi duyệt đơn ở trạng thái Nháp!'))
            if not record.don_muon_tai_san_ids:
                raise UserError(_('Vui lòng thêm ít nhất một tài sản vào đơn mượn!'))
            
            # Cập nhật trạng thái đơn
            record.write({'trang_thai': 'cho_duyet'})
            
            # Tạo phiếu trong Quản lý mượn trả tài sản
            muon_tra_lines = []
            for line in record.don_muon_tai_san_ids:
                muon_tra_lines.append((0, 0, {
                    'phan_bo_tai_san_id': line.phan_bo_tai_san_id.id if line.phan_bo_tai_san_id else False,
                    'ghi_chu': line.ghi_chu or '',
                }))
            
            muon_tra = self.env['muon_tra_tai_san'].create({
                'ma_don_muon_id': record.id,
                'ten_phieu_muon_tra': f"Duyệt đơn mượn {record.ma_don_muon} - {record.ten_don_muon}",
                'phong_ban_cho_muon_id': record.phong_ban_cho_muon_id.id,
                'nhan_vien_muon_id': record.nhan_vien_muon_id.id,
                'thoi_gian_muon': record.thoi_gian_muon,
                'thoi_gian_tra_du_kien': record.thoi_gian_tra,
                'ly_do_muon': record.ly_do,
                'trang_thai': 'cho_duyet',
                'muon_tra_line_ids': muon_tra_lines,
            })
            
            record.message_post(body=_('📤 Đơn mượn đã được gửi để phê duyệt. Mã phiếu: %s') % muon_tra.ma_phieu_muon_tra)
    
    def action_duyet(self):
        """Duyệt đơn mượn"""
        for record in self:
            if record.trang_thai != 'cho_duyet':
                raise UserError(_('Chỉ có thể duyệt đơn đang chờ duyệt!'))
            record.write({
                'trang_thai': 'da_duyet',
                'nguoi_duyet_id': self.env.user.id,
                'ngay_duyet': fields.Datetime.now(),
            })
            record.message_post(body=_('✅ Đơn mượn đã được duyệt bởi %s.') % self.env.user.name)
    
    def action_tu_choi(self):
        """Từ chối đơn mượn"""
        for record in self:
            if record.trang_thai != 'cho_duyet':
                raise UserError(_('Chỉ có thể từ chối đơn đang chờ duyệt!'))
            # Mở wizard yêu cầu nhập lý do
            return {
                'name': 'Lý do từ chối',
                'type': 'ir.actions.act_window',
                'res_model': 'don_muon_tu_choi_wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {'default_don_muon_id': record.id}
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
            record.message_post(body=_('❌ Đơn mượn đã bị từ chối. Lý do: %s') % ly_do)
    
    def action_xac_nhan_muon(self):
        """Xác nhận đã cho mượn tài sản"""
        for record in self:
            if record.trang_thai != 'da_duyet':
                raise UserError(_('Chỉ có thể xác nhận mượn cho đơn đã duyệt!'))
            
            now = fields.Datetime.now()
            record.write({
                'trang_thai': 'dang_muon',
                'thoi_gian_muon': now,
            })
            
            # Cập nhật trạng thái từng tài sản và ghi nhận thời gian, người giao
            for line in record.don_muon_tai_san_ids:
                if line.phan_bo_tai_san_id:
                    line.phan_bo_tai_san_id.write({'tinh_trang': 'dang_muon'})
                    line.write({
                        'thoi_gian_cho_muon': now,
                        'nguoi_giao_id': self.env.user.id,
                        'trang_thai_line': 'dang_muon',
                    })
            
            record.message_post(body=_('📦 Tài sản đã được cho mượn lúc %s bởi %s.') % (
                now.strftime('%d/%m/%Y %H:%M'), self.env.user.name))
    
    def action_xac_nhan_tra(self):
        """Mở wizard xác nhận trả tài sản với tình trạng"""
        self.ensure_one()
        if self.trang_thai != 'dang_muon':
            raise UserError(_('Chỉ có thể xác nhận trả cho đơn đang mượn!'))
        
        return {
            'name': 'Xác nhận trả tài sản',
            'type': 'ir.actions.act_window',
            'res_model': 'xac_nhan_tra_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_don_muon_id': self.id}
        }
    
    def action_xac_nhan_tra_hoan_tat(self):
        """Hoàn tất xác nhận trả tài sản (được gọi từ wizard)"""
        for record in self:
            now = fields.Datetime.now()
            record.write({
                'trang_thai': 'da_tra',
                'ngay_tra_thuc_te': now,
                'nguoi_xac_nhan_tra_id': self.env.user.id,
            })
            
            # Cập nhật trạng thái từng tài sản
            for line in record.don_muon_tai_san_ids:
                if line.phan_bo_tai_san_id:
                    # Cập nhật tình trạng phan_bo dựa trên tình trạng sau trả
                    tinh_trang_moi = 'binh_thuong'
                    if line.tinh_trang_sau_tra == 'hu_hong':
                        tinh_trang_moi = 'hu_hong'
                    elif line.tinh_trang_sau_tra == 'mat':
                        tinh_trang_moi = 'mat'
                    
                    line.phan_bo_tai_san_id.write({'tinh_trang': tinh_trang_moi})
                    line.write({
                        'thoi_gian_tra_thuc_te': now,
                        'nguoi_nhan_tra_id': self.env.user.id,
                        'trang_thai_line': 'da_tra' if line.tinh_trang_sau_tra not in ['mat', 'hu_hong'] else ('mat' if line.tinh_trang_sau_tra == 'mat' else 'hong'),
                    })
            
            record.message_post(body=_('✅ Tài sản đã được trả lúc %s. Người nhận: %s.') % (
                now.strftime('%d/%m/%Y %H:%M'), self.env.user.name))
    
    def action_huy(self):
        """Hủy đơn mượn"""
        for record in self:
            if record.trang_thai in ['dang_muon', 'da_tra']:
                raise UserError(_('Không thể hủy đơn đang mượn hoặc đã trả!'))
            record.write({'trang_thai': 'huy'})
            record.message_post(body=_('🚫 Đơn mượn đã bị hủy.'))
    
    def action_dat_lai_nhap(self):
        """Đặt lại về trạng thái nháp"""
        for record in self:
            if record.trang_thai not in ['tu_choi', 'huy']:
                raise UserError(_('Chỉ có thể đặt lại đơn bị từ chối hoặc đã hủy!'))
            record.write({
                'trang_thai': 'nhap',
                'nguoi_duyet_id': False,
                'ngay_duyet': False,
                'ly_do_tu_choi': False,
            })
            record.message_post(body=_('📝 Đơn mượn đã được đặt lại về trạng thái Nháp.'))