# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date

class PheDuyetMuaTaiSan(models.Model):
    """
    Model phê duyệt mua tài sản - Bước 2 trong luồng mua thiết bị
    Nhận đơn từ module tài sản → Phê duyệt → Tự động tạo tài sản + ghi nhận tài chính
    """
    _name = 'phe_duyet_mua_tai_san'
    _description = 'Phê duyệt mua tài sản'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'ma_phe_duyet'
    _order = 'ngay_tao desc'

    # ============ THÔNG TIN CƠ BẢN ============
    ma_phe_duyet = fields.Char(
        string='Mã phê duyệt',
        required=True,
        readonly=True,
        copy=False,
        default='New',
        tracking=True,
        help='Mã tự động tạo khi lưu đơn phê duyệt'
    )
    
    ngay_tao = fields.Date(
        string='Ngày tạo',
        default=fields.Date.context_today,
        required=True,
        readonly=True,
        tracking=True
    )
    
    # ============ LIÊN KẾT ĐỀ XUẤT GỐC ============
    de_xuat_mua_id = fields.Many2one(
        'de_xuat_mua_tai_san',
        string='Đề xuất mua',
        required=False,  # ← Thay đổi thành False để tránh lỗi
        readonly=True,
        ondelete='set null',  # ← Thay đổi để tránh lỗi restrict
        tracking=True,
        help='Đề xuất mua tài sản từ module quản lý tài sản'
    )
    
    ma_de_xuat = fields.Char(
        string='Mã đề xuất',
        compute='_compute_ma_de_xuat',
        readonly=True,
        store=False,
        help='Mã đề xuất gốc (nếu có)'
    )
    
    # ============ THÔNG TIN TỪ ĐỀ XUẤT ============
    ten_de_xuat = fields.Char(
        string='Tiêu đề',
        readonly=True,
        tracking=True
    )
    
    ngay_de_xuat = fields.Date(
        string='Ngày đề xuất',
        readonly=True
    )
    
    nguoi_de_xuat_id = fields.Many2one(
        'res.users',
        string='Người đề xuất',
        readonly=True,
        ondelete='set null'
    )
    
    phong_ban_id = fields.Many2one(
        'phong_ban',
        string='Phòng ban đề xuất',
        readonly=True,
        ondelete='set null'
    )
    
    # ============ CHI TIẾT THIẾT BỊ ============
    line_ids = fields.One2many(
        'phe_duyet_mua_tai_san.line',
        'phe_duyet_id',
        string='Chi tiết thiết bị',
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    
    # ============ TỔNG TIỀN ============
    tong_gia_tri = fields.Float(
        string='Tổng giá trị',
        readonly=True,
        tracking=True
    )
    
    don_vi_tien_te = fields.Selection([
        ('vnd', 'VNĐ'),
        ('usd', 'USD'),
    ], string='Đơn vị tiền tệ', readonly=True)
    
    # ============ LÝ DO VÀ MÔ TẢ ============
    ly_do = fields.Text(
        string='Lý do đề xuất',
        readonly=True
    )
    
    mo_ta = fields.Html(
        string='Mô tả chi tiết',
        readonly=True
    )
    
    ngay_du_kien_nhan = fields.Date(
        string='Ngày dự kiến nhận hàng',
        readonly=True
    )
    
    # ============ TRẠNG THÁI ============
    state = fields.Selection([
        ('draft', 'Chờ phê duyệt'),
        ('approved', 'Đã phê duyệt'),
        ('rejected', 'Từ chối'),
        ('done', 'Hoàn thành'),
        ('cancelled', 'Đã hủy'),
    ], string='Trạng thái', default='draft', required=True, tracking=True)
    
    # ============ PHÊ DUYỆT ============
    nguoi_phe_duyet_id = fields.Many2one(
        'res.users',
        string='Người phê duyệt',
        readonly=True,
        tracking=True,
        ondelete='set null'
    )
    
    ngay_phe_duyet = fields.Date(
        string='Ngày phê duyệt',
        readonly=True,
        tracking=True
    )
    
    ghi_chu_phe_duyet = fields.Text(
        string='Ghi chú phê duyệt',
        tracking=True
    )
    
    # ============ TÀI CHÍNH ============
    # Tài khoản kế toán
    tk_tai_san_id = fields.Many2one(
        'account.account',
        string='TK Tài sản cố định',
        domain="[('deprecated', '=', False)]",
        help='Tài khoản ghi Nợ khi mua tài sản (VD: 211 - TSCĐ hữu hình)',
        ondelete='restrict'
    )
    
    tk_nguon_von_id = fields.Many2one(
        'account.account',
        string='TK Nguồn vốn',
        domain="[('deprecated', '=', False)]",
        help='Tài khoản ghi Có khi mua tài sản (VD: 112 - Tiền mặt, 1121 - Tiền gửi ngân hàng)',
        ondelete='restrict'
    )
    
    journal_id = fields.Many2one(
        'account.journal',
        string='Sổ nhật ký',
        help='Sổ nhật ký ghi nhận giao dịch mua tài sản',
        ondelete='restrict'
    )
    
    # Bút toán đã tạo
    but_toan_id = fields.Many2one(
        'account.move',
        string='Bút toán ghi nhận',
        readonly=True,
        tracking=True,
        help='Bút toán ghi nhận mua tài sản',
        ondelete='set null'
    )
    
    # Liên kết đến bảng quản trị tài chính (nếu có)
    tai_khoan_quan_tri_ids = fields.One2many(
        'tai_khoan_quan_tri',
        'phe_duyet_mua_id',
        string='Ghi nhận quản trị',
        readonly=True
    )
    
    # ============ TÀI SẢN ĐÃ TẠO ============
    tai_san_ids = fields.Many2many(
        'tai_san',
        string='Tài sản đã tạo',
        readonly=True,
        help='Danh sách tài sản được tạo sau khi phê duyệt'
    )
    
    tai_san_count = fields.Integer(
        string='Số lượng tài sản',
        compute='_compute_tai_san_count'
    )
    
    # ============ KHẤU HAO ============
    khau_hao_ids = fields.One2many(
        'khau_hao_tai_san',
        'phe_duyet_mua_id',
        string='Lịch khấu hao',
        readonly=True,
        help='Lịch khấu hao tự động cho các tài sản'
    )
    
    # ============ COMPUTE METHODS ============
    @api.depends('de_xuat_mua_id', 'de_xuat_mua_id.ma_de_xuat')
    def _compute_ma_de_xuat(self):
        """
        Compute mã đề xuất an toàn, tránh lỗi _unknown
        
        Xử lý:
        - Kiểm tra de_xuat_mua_id tồn tại
        - Kiểm tra record có exists() không
        - Xử lý exception khi truy cập thuộc tính
        - Luôn gán giá trị (False nếu không có)
        """
        for record in self:
            try:
                # Kiểm tra 1: de_xuat_mua_id có giá trị không
                if not record.de_xuat_mua_id:
                    record.ma_de_xuat = False
                    continue
                
                # Kiểm tra 2: Record có tồn tại trong DB không
                if not record.de_xuat_mua_id.exists():
                    record.ma_de_xuat = False
                    continue
                
                # Kiểm tra 3: Truy cập an toàn thuộc tính ma_de_xuat
                ma = record.de_xuat_mua_id.ma_de_xuat
                record.ma_de_xuat = ma if ma else False
                
            except AttributeError:
                # Nếu gặp lỗi AttributeError (_unknown object)
                record.ma_de_xuat = False
            except Exception:
                # Bất kỳ exception nào khác
                record.ma_de_xuat = False
    
    @api.depends('tai_san_ids')
    def _compute_tai_san_count(self):
        for record in self:
            record.tai_san_count = len(record.tai_san_ids)
    
    # ============ ONCHANGE METHODS ============
    @api.onchange('de_xuat_mua_id')
    def _onchange_de_xuat_mua_id(self):
        """
        Xử lý khi thay đổi đề xuất mua
        Đảm bảo không gây lỗi _unknown object
        """
        # Không làm gì nếu không có đề xuất
        if not self.de_xuat_mua_id:
            return
        
        # Kiểm tra đề xuất có tồn tại không
        if not self.de_xuat_mua_id.exists():
            self.de_xuat_mua_id = False
            return
        
        # Trigger recompute cho ma_de_xuat
        # Field sẽ tự động compute an toàn qua _compute_ma_de_xuat
        pass
    
    # ============ CRUD METHODS ============
    @api.model
    def create(self, vals):
        # Tạo mã phê duyệt
        if vals.get('ma_phe_duyet', 'New') == 'New':
            vals['ma_phe_duyet'] = self.env['ir.sequence'].next_by_code('phe_duyet_mua_tai_san') or 'New'
        
        # Xử lý an toàn các trường Many2one - đảm bảo không có giá trị invalid
        many2one_fields = ['de_xuat_mua_id', 'nguoi_de_xuat_id', 'phong_ban_id', 
                           'nguoi_phe_duyet_id', 'tk_tai_san_id', 'tk_nguon_von_id', 
                           'journal_id', 'but_toan_id']
        
        for field_name in many2one_fields:
            if field_name in vals:
                field_value = vals[field_name]
                # Nếu là False, None, hoặc 0 thì set về False
                if not field_value or field_value == 0:
                    vals[field_name] = False
                # Nếu là tuple (command), giữ nguyên
                elif isinstance(field_value, (list, tuple)):
                    continue
                # Nếu là int, kiểm tra record có tồn tại không
                elif isinstance(field_value, int):
                    field_obj = self._fields[field_name]
                    if hasattr(field_obj, 'comodel_name'):
                        model_name = field_obj.comodel_name
                        if model_name and model_name in self.env:
                            if not self.env[model_name].browse(field_value).exists():
                                vals[field_name] = False
        
        # Xử lý line_ids an toàn
        if 'line_ids' in vals:
            safe_lines = []
            for line_cmd in vals['line_ids']:
                if isinstance(line_cmd, (list, tuple)) and len(line_cmd) >= 3:
                    cmd, _, line_vals = line_cmd[0], line_cmd[1], line_cmd[2] if len(line_cmd) > 2 else {}
                    if cmd == 0 and isinstance(line_vals, dict):
                        # Xử lý an toàn danh_muc_ts_id trong line
                        if 'danh_muc_ts_id' in line_vals:
                            dm_val = line_vals['danh_muc_ts_id']
                            if not dm_val or dm_val == 0:
                                line_vals['danh_muc_ts_id'] = False
                            elif isinstance(dm_val, int):
                                if 'danh_muc_tai_san' in self.env:
                                    if not self.env['danh_muc_tai_san'].browse(dm_val).exists():
                                        line_vals['danh_muc_ts_id'] = False
                    safe_lines.append(line_cmd)
            vals['line_ids'] = safe_lines
        
        return super(PheDuyetMuaTaiSan, self).create(vals)
    
    @api.model
    def default_get(self, fields_list):
        """Thiết lập giá trị mặc định cho tài khoản"""
        res = super(PheDuyetMuaTaiSan, self).default_get(fields_list)
        
        # Tài khoản tài sản cố định mặc định (211)
        if 'tk_tai_san_id' in fields_list:
            tk_ts = self.env['account.account'].search([
                ('code', '=like', '211%'),
                ('deprecated', '=', False)
            ], limit=1)
            if tk_ts:
                res['tk_tai_san_id'] = tk_ts.id
        
        # Tài khoản tiền mặt mặc định (112)
        if 'tk_nguon_von_id' in fields_list:
            tk_tien = self.env['account.account'].search([
                ('code', '=like', '112%'),
                ('deprecated', '=', False)
            ], limit=1)
            if tk_tien:
                res['tk_nguon_von_id'] = tk_tien.id
        
        # Sổ nhật ký mặc định
        if 'journal_id' in fields_list:
            journal = self.env['account.journal'].search([
                ('type', '=', 'purchase')
            ], limit=1)
            if not journal:
                journal = self.env['account.journal'].search([
                    ('type', '=', 'general')
                ], limit=1)
            if journal:
                res['journal_id'] = journal.id
        
        return res
    
    # ============ ACTION METHODS ============
    def action_approve(self):
        """Phê duyệt đơn mua tài sản"""
        for record in self:
            if record.state != 'draft':
                raise UserError(_('Chỉ có thể phê duyệt đơn đang chờ phê duyệt.'))
            
            # Tự động set giá trị mặc định nếu chưa có
            vals_to_update = {}
            
            # Bước 1: Tìm hoặc set journal trước
            if not record.journal_id:
                journal = self.env['account.journal'].search([
                    ('type', '=', 'general')  # Dùng sổ nhật ký chung để tránh lỗi
                ], limit=1)
                if not journal:
                    journal = self.env['account.journal'].search([
                        ('type', '=', 'purchase')
                    ], limit=1)
                if journal:
                    vals_to_update['journal_id'] = journal.id
                else:
                    raise UserError(_('Không tìm thấy sổ nhật ký. Vui lòng tạo sổ nhật ký General hoặc Purchase trước.'))
            else:
                journal = record.journal_id
            
            # Bước 2: Tìm tài khoản tài sản cố định (không phụ thuộc journal)
            if not record.tk_tai_san_id:
                tk_ts = self.env['account.account'].search([
                    ('code', '=like', '211%'),
                    ('deprecated', '=', False)
                ], limit=1)
                if not tk_ts:
                    # Thử tìm bất kỳ tài khoản Fixed Assets nào
                    tk_ts = self.env['account.account'].search([
                        ('user_type_id.name', 'ilike', 'fixed'),
                        ('deprecated', '=', False)
                    ], limit=1)
                if tk_ts:
                    vals_to_update['tk_tai_san_id'] = tk_ts.id
                else:
                    raise UserError(_('Không tìm thấy tài khoản tài sản cố định. Vui lòng tạo tài khoản 211 trước.'))
            
            # Bước 3: Tìm tài khoản nguồn vốn PHÙ HỢP với journal
            if not record.tk_nguon_von_id:
                # Tìm tài khoản được phép dùng trong journal này
                domain = [
                    ('deprecated', '=', False),
                    '|',
                    ('code', '=like', '112%'),
                    ('code', '=like', '111%')
                ]
                
                # Nếu có journal_id, tìm account phù hợp với allowed_journal_ids
                if journal:
                    # Tìm account có journal trong allowed_journal_ids
                    accounts = self.env['account.account'].search(domain)
                    tk_tien = False
                    for acc in accounts:
                        if not acc.allowed_journal_ids or journal in acc.allowed_journal_ids:
                            tk_tien = acc
                            break
                    
                    # Nếu không tìm thấy, dùng account bất kỳ thuộc loại Cash/Bank
                    if not tk_tien:
                        tk_tien = self.env['account.account'].search([
                            ('deprecated', '=', False),
                            ('user_type_id.type', 'in', ['bank', 'cash']),
                            '|',
                            ('allowed_journal_ids', '=', False),
                            ('allowed_journal_ids', 'in', journal.ids)
                        ], limit=1)
                else:
                    tk_tien = self.env['account.account'].search(domain, limit=1)
                
                if tk_tien:
                    vals_to_update['tk_nguon_von_id'] = tk_tien.id
                else:
                    raise UserError(_(
                        'Không tìm thấy tài khoản nguồn vốn phù hợp.\n\n'
                        'Vui lòng:\n'
                        '1. Tạo tài khoản 112 hoặc 111\n'
                        '2. Vào Accounting → Configuration → Journals\n'
                        '3. Chọn journal "%s"\n'
                        '4. Thêm tài khoản 112 vào "Allowed Accounts" hoặc để trống'
                    ) % (journal.name if journal else 'General'))
            
            # Cập nhật các trường nếu cần
            if vals_to_update:
                record.write(vals_to_update)
            
            # Cập nhật trạng thái
            record.write({
                'state': 'approved',
                'nguoi_phe_duyet_id': self.env.user.id,
                'ngay_phe_duyet': fields.Date.today(),
            })
            
            # ===== BƯỚC 1: TẠO TÀI SẢN TRONG MODULE QUẢN LÝ TÀI SẢN =====
            # Đây là bước QUAN TRỌNG NHẤT - phải thành công
            created_assets = False
            try:
                created_assets = record._create_assets()
                # Commit ngay lập tức để đảm bảo tài sản được lưu vĩnh viễn
                # Ngay cả khi các bước sau bị lỗi, tài sản vẫn tồn tại
                self.env.cr.commit()
            except Exception as e:
                # Nếu không tạo được tài sản, rollback và báo lỗi
                self.env.cr.rollback()
                # Khôi phục trạng thái về draft
                record.write({'state': 'draft', 'nguoi_phe_duyet_id': False, 'ngay_phe_duyet': False})
                raise UserError(_('Lỗi khi tạo tài sản trong module quản lý tài sản:\n%s\n\nVui lòng kiểm tra:\n- Module Quản lý tài sản đã được cài đặt\n- Danh mục tài sản đã được thiết lập\n- Các trường bắt buộc đã đầy đủ') % str(e))
            
            # ===== BƯỚC 2: GHI NHẬN TÀI CHÍNH (SỔ CÁI) =====
            # Tạo bút toán kế toán
            try:
                record._create_journal_entry()
                self.env.cr.commit()  # Commit ngay nếu thành công
            except Exception as e:
                # Nếu gặp lỗi, chỉ log warning, không rollback tài sản
                # Tài sản đã tạo ở bước 1 sẽ vẫn tồn tại
                record.message_post(
                    body=_('Cảnh báo: Không tạo được bút toán kế toán. Lỗi: %s\nTài sản đã được tạo thành công.') % str(e),
                    subject=_('Cảnh báo bút toán')
                )
            
            # ===== BƯỚC 3: TẠO LỊCH KHẤU HAO =====
            try:
                record._create_depreciation_schedule()
                self.env.cr.commit()  # Commit nếu thành công
            except Exception as e:
                # Log lỗi nhưng tiếp tục
                record.message_post(
                    body=_('Cảnh báo: Không tạo được lịch khấu hao. Lỗi: %s\nBạn có thể tạo khấu hao thủ công sau.') % str(e),
                    subject=_('Cảnh báo khấu hao')
                )
            
            # ===== BƯỚC 4: GHI NHẬN KẾ TOÁN QUẢN TRỊ =====
            try:
                record._create_management_accounting()
                self.env.cr.commit()  # Commit nếu thành công
            except Exception as e:
                # Log lỗi nhưng tiếp tục
                record.message_post(
                    body=_('Cảnh báo: Không ghi nhận được vào kế toán quản trị. Lỗi: %s') % str(e),
                    subject=_('Cảnh báo kế toán quản trị')
                )
            
            # ===== BƯỚC 5: CẬP NHẬT ĐỀ XUẤT GỐC =====
            try:
                if record.de_xuat_mua_id and record.de_xuat_mua_id.exists():
                    record.de_xuat_mua_id._on_approval_approved()
                    # Đồng bộ tài sản vào đề xuất
                    if created_assets:
                        record.de_xuat_mua_id.write({'tai_san_ids': [(6, 0, created_assets.ids)]})
                    self.env.cr.commit()
            except Exception as e:
                # Bỏ qua nếu không thể cập nhật đề xuất
                record.message_post(
                    body=_('Cảnh báo: Không cập nhật được đề xuất gốc. Lỗi: %s') % str(e),
                    subject=_('Cảnh báo đề xuất')
                )
            
            # ===== HOÀN THÀNH =====
            record.write({'state': 'done'})
            self.env.cr.commit()
            
            # Gửi thông báo thành công
            asset_count = len(created_assets) if created_assets else 0
            record.message_post(
                body=_('✅ Phê duyệt thành công!\n\n'
                       '📦 Đã tạo %s tài sản trong module Quản lý tài sản\n'
                       '💰 Đã ghi nhận giao dịch vào hệ thống tài chính\n'
                       '📊 Tài sản sẵn sàng cho: Tính khấu hao, Kiểm kê, Mượn trả, Thanh lý, Bảo trì') % asset_count,
                subject=_('Phê duyệt hoàn tất')
            )
    
    def action_reject(self):
        """Từ chối đơn mua tài sản"""
        for record in self:
            if record.state != 'draft':
                raise UserError(_('Chỉ có thể từ chối đơn đang chờ phê duyệt.'))
            
            record.write({
                'state': 'rejected',
                'nguoi_phe_duyet_id': self.env.user.id,
                'ngay_phe_duyet': fields.Date.today(),
            })
            
            # Cập nhật trạng thái đề xuất gốc
            if record.de_xuat_mua_id and record.de_xuat_mua_id.exists():
                try:
                    record.de_xuat_mua_id._on_approval_rejected()
                except:
                    pass  # Bỏ qua nếu không thể cập nhật đề xuất
            
            # Gửi thông báo
            record.message_post(
                body=_('Đơn mua tài sản đã bị từ chối.'),
                subject=_('Đơn bị từ chối')
            )
    
    def action_cancel(self):
        """Hủy đơn phê duyệt"""
        for record in self:
            if record.state in ['approved', 'done']:
                raise UserError(_('Không thể hủy đơn đã được phê duyệt hoàn thành.'))
            record.state = 'cancelled'
    
    def unlink(self):
        """
        Xóa đơn phê duyệt
        Khi xóa, cần reset trạng thái đề xuất gốc về draft để có thể xóa
        """
        for record in self:
            # Gọi callback ở module tài sản để reset trạng thái
            if record.de_xuat_mua_id and record.de_xuat_mua_id.exists():
                try:
                    record.de_xuat_mua_id._on_approval_deleted()
                except Exception as e:
                    # Log warning nhưng không block xóa
                    from odoo import _logger
                    _logger.warning(f"Could not reset proposal {record.de_xuat_mua_id.id}: {e}")
        
        return super(PheDuyetMuaTaiSan, self).unlink()
    
    def _create_assets(self):
        """
        Tự động tạo tài sản trong module quản lý tài sản
        
        Luồng:
        1. Kiểm tra module quản_ly_tai_san đã cài đặt
        2. Tạo tài sản theo từng dòng chi tiết
        3. Mỗi dòng tạo nhiều tài sản theo số lượng
        4. Lưu liên kết tài sản vào đơn phê duyệt
        5. Đồng bộ tài sản về đề xuất gốc
        
        Returns:
            recordset: Danh sách tài sản đã tạo (tai_san)
        """
        self.ensure_one()
        
        # Kiểm tra module quản lý tài sản
        if not self.env['ir.module.module'].search([
            ('name', '=', 'quan_ly_tai_san'), 
            ('state', '=', 'installed')
        ]):
            raise UserError(_('Module Quản lý tài sản chưa được cài đặt.\n\nVui lòng cài đặt module "quan_ly_tai_san" trước khi phê duyệt mua tài sản.'))
        
        # Kiểm tra có chi tiết thiết bị không
        if not self.line_ids:
            raise UserError(_('Không có chi tiết thiết bị nào để tạo tài sản.\n\nVui lòng thêm thiết bị vào đơn phê duyệt.'))
        
        tai_san_obj = self.env['tai_san']
        created_assets = self.env['tai_san']
        
        # Tạo tài sản cho từng dòng chi tiết
        for line in self.line_ids:
            # Validate dữ liệu
            if not line.danh_muc_ts_id:
                raise UserError(_('Dòng "%s" chưa có danh mục tài sản.\n\nVui lòng chọn danh mục tài sản cho tất cả các dòng.') % line.ten_thiet_bi)
            
            if line.so_luong <= 0:
                raise UserError(_('Dòng "%s" có số lượng không hợp lệ.\n\nSố lượng phải lớn hơn 0.') % line.ten_thiet_bi)
            
            # Tạo từng tài sản theo số lượng
            for i in range(int(line.so_luong)):
                # Tạo mã tài sản duy nhất
                asset_code = f"{self.ma_phe_duyet}-{line.sequence or line.id}-{i+1:03d}"
                
                # Chuẩn bị dữ liệu tài sản
                asset_vals = {
                    'ma_tai_san': asset_code,
                    'ten_tai_san': line.ten_thiet_bi,
                    'ngay_mua_ts': self.ngay_phe_duyet or fields.Date.today(),
                    'don_vi_tien_te': self.don_vi_tien_te or 'vnd',
                    'gia_tri_ban_dau': line.don_gia,
                    'gia_tri_hien_tai': line.don_gia,
                    'danh_muc_ts_id': line.danh_muc_ts_id.id,
                    'pp_khau_hao': line.pp_khau_hao or 'none',
                    'thoi_gian_su_dung': 0,  # Mới mua nên = 0
                    'thoi_gian_toi_da': line.thoi_gian_su_dung or 5,
                    'ty_le_khau_hao': line.ty_le_khau_hao or 20.0,
                    'don_vi_tinh': line.don_vi_tinh or 'Chiếc',
                    'ghi_chu': (
                        f'✅ Mua từ phê duyệt: {self.ma_phe_duyet}\n'
                        f'📋 Đề xuất gốc: {self.ma_de_xuat or "N/A"}\n'
                        f'📅 Ngày phê duyệt: {self.ngay_phe_duyet}\n'
                        f'👤 Người phê duyệt: {self.nguoi_phe_duyet_id.name if self.nguoi_phe_duyet_id else "N/A"}\n'
                        f'🏢 Phòng ban: {self.phong_ban_id.name if self.phong_ban_id else "N/A"}\n'
                        f'📝 Mô tả: {line.mo_ta or "Không có"}'
                    ),
                }
                
                # Tạo tài sản
                try:
                    asset = tai_san_obj.create(asset_vals)
                    created_assets |= asset
                except Exception as e:
                    # Nếu lỗi khi tạo tài sản, báo rõ dòng nào bị lỗi
                    raise UserError(_(
                        'Lỗi khi tạo tài sản "%s" (số %s/%s):\n%s\n\n'
                        'Dữ liệu:\n'
                        '- Mã: %s\n'
                        '- Tên: %s\n'
                        '- Danh mục: %s\n'
                        '- Giá trị: %s %s'
                    ) % (
                        line.ten_thiet_bi, i+1, int(line.so_luong), str(e),
                        asset_code, line.ten_thiet_bi, 
                        line.danh_muc_ts_id.name if line.danh_muc_ts_id else 'N/A',
                        line.don_gia, self.don_vi_tien_te or 'VND'
                    ))
        
        # Kiểm tra đã tạo tài sản thành công chưa
        if not created_assets:
            raise UserError(_('Không tạo được tài sản nào.\n\nVui lòng kiểm tra lại dữ liệu đơn phê duyệt.'))
        
        # Lưu liên kết tài sản vào đơn phê duyệt (quan trọng!)
        self.write({'tai_san_ids': [(6, 0, created_assets.ids)]})
        
        # Đồng bộ tài sản về đề xuất gốc (nếu có)
        if self.de_xuat_mua_id and self.de_xuat_mua_id.exists():
            try:
                # Kiểm tra xem đề xuất có trường tai_san_ids không
                if hasattr(self.de_xuat_mua_id, 'tai_san_ids'):
                    self.de_xuat_mua_id.write({'tai_san_ids': [(6, 0, created_assets.ids)]})
            except Exception as e:
                # Chỉ log warning, không block luồng chính
                self.message_post(
                    body=_('Cảnh báo: Không đồng bộ được tài sản về đề xuất gốc. Lỗi: %s') % str(e),
                    subject=_('Cảnh báo đồng bộ')
                )
        
        return created_assets
    
    def _create_journal_entry(self):
        """Tự động ghi nhận sổ cái và dòng tiền"""
        self.ensure_one()
        
        if self.tong_gia_tri <= 0:
            raise UserError(_('Tổng giá trị phải lớn hơn 0 để tạo bút toán.'))
        
        # Tạo bút toán
        move_vals = {
            'journal_id': self.journal_id.id if self.journal_id else False,
            'date': self.ngay_phe_duyet or fields.Date.today(),
            'ref': f'Mua tài sản - {self.ma_phe_duyet}',
            'line_ids': [
                # Nợ TK Tài sản cố định
                (0, 0, {
                    'name': f'Mua tài sản: {self.ten_de_xuat}',
                    'account_id': self.tk_tai_san_id.id if self.tk_tai_san_id else False,
                    'debit': self.tong_gia_tri,
                    'credit': 0,
                }),
                # Có TK Nguồn vốn
                (0, 0, {
                    'name': f'Thanh toán mua tài sản: {self.ten_de_xuat}',
                    'account_id': self.tk_nguon_von_id.id if self.tk_nguon_von_id else False,
                    'debit': 0,
                    'credit': self.tong_gia_tri,
                }),
            ]
        }
        
        move = self.env['account.move'].create(move_vals)
        move.action_post()  # Đăng bút toán
        
        self.but_toan_id = move.id
        
        return move
    
    def _create_depreciation_schedule(self):
        """Tạo lịch khấu hao tự động cho các tài sản"""
        self.ensure_one()
        
        khau_hao_obj = self.env['khau_hao_tai_san']
        
        for asset in self.tai_san_ids:
            if asset.pp_khau_hao == 'none':
                continue
            
            # Tạo bản ghi khấu hao với đầy đủ trường bắt buộc
            khau_hao_vals = {
                'tai_san_id': asset.id,
                'phe_duyet_mua_id': self.id,
                'ngay_bat_dau': self.ngay_phe_duyet or fields.Date.today(),
                'gia_tri_ban_dau': asset.gia_tri_ban_dau,
                'thoi_gian_khau_hao': asset.thoi_gian_toi_da or 0,
                'so_nam_khau_hao': asset.thoi_gian_toi_da or 5,  # Thêm trường bắt buộc
                'ty_le_khau_hao': asset.ty_le_khau_hao or 20.0,
                'phuong_phap': asset.pp_khau_hao or 'straight-line',
            }
            
            khau_hao_obj.create(khau_hao_vals)
    
    def _create_management_accounting(self):
        """Ghi nhận vào kế toán quản trị"""
        self.ensure_one()
        
        # Kiểm tra model có tồn tại không
        if 'tai_khoan_quan_tri' not in self.env:
            return
        
        tk_qt_obj = self.env['tai_khoan_quan_tri']
        
        # Tạo bản ghi kế toán quản trị với đầy đủ trường bắt buộc
        tk_qt_vals = {
            'ten_tai_khoan': f'Mua tài sản - {self.ma_phe_duyet}',
            'ma_tai_khoan': f'TK-{self.ma_phe_duyet}',  # Tạo mã tự động
            'phe_duyet_mua_id': self.id,
            'ngay_ghi_nhan': self.ngay_phe_duyet or fields.Date.today(),
            'loai_giao_dich': 'mua_tai_san',
            'mo_ta': f'Mua tài sản: {self.ten_de_xuat or ""}',
            'so_tien': self.tong_gia_tri or 0.0,
            'don_vi_tien_te': self.don_vi_tien_te or 'vnd',
            'phong_ban_id': self.phong_ban_id.id if self.phong_ban_id else False,
        }
        
        tk_qt_obj.create(tk_qt_vals)
    
    # ============ VIEW ACTIONS ============
    def action_view_assets(self):
        """Xem tài sản đã tạo"""
        self.ensure_one()
        return {
            'name': _('Tài sản đã tạo'),
            'type': 'ir.actions.act_window',
            'res_model': 'tai_san',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.tai_san_ids.ids)],
            'context': {'create': False}
        }
    
    def action_view_journal_entry(self):
        """Xem bút toán đã tạo"""
        self.ensure_one()
        if not self.but_toan_id:
            raise UserError(_('Chưa có bút toán nào được tạo.'))
        
        return {
            'name': _('Bút toán ghi nhận'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': self.but_toan_id.id if self.but_toan_id else False,
            'context': {'create': False}
        }
    
    def action_view_depreciation(self):
        """Xem lịch khấu hao"""
        self.ensure_one()
        return {
            'name': _('Lịch khấu hao tài sản'),
            'type': 'ir.actions.act_window',
            'res_model': 'khau_hao_tai_san',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.khau_hao_ids.ids)],
            'context': {'create': False}
        }
    
    def action_view_source_proposal(self):
        """Xem đề xuất gốc"""
        self.ensure_one()
        if not self.de_xuat_mua_id:
            raise UserError(_('Không tìm thấy đề xuất gốc.'))
        
        return {
            'name': _('Đề xuất mua tài sản'),
            'type': 'ir.actions.act_window',
            'res_model': 'de_xuat_mua_tai_san',
            'view_mode': 'form',
            'res_id': self.de_xuat_mua_id.id if self.de_xuat_mua_id else False,
            'target': 'current',
        }


class PheDuyetMuaTaiSanLine(models.Model):
    """Chi tiết phê duyệt mua tài sản"""
    _name = 'phe_duyet_mua_tai_san.line'
    _description = 'Chi tiết phê duyệt mua tài sản'
    _order = 'sequence, id'
    
    sequence = fields.Integer(string='STT', default=10)
    
    phe_duyet_id = fields.Many2one(
        'phe_duyet_mua_tai_san',
        string='Phê duyệt',
        required=True,
        ondelete='cascade'
    )
    
    # ============ THÔNG TIN THIẾT BỊ ============
    ten_thiet_bi = fields.Char(
        string='Tên thiết bị',
        required=True,
        readonly=True
    )
    
    danh_muc_ts_id = fields.Many2one(
        'danh_muc_tai_san',
        string='Danh mục tài sản',
        required=True,
        readonly=True,
        ondelete='restrict'
    )
    
    mo_ta = fields.Text(
        string='Mô tả',
        readonly=True
    )
    
    thong_so_ky_thuat = fields.Text(
        string='Thông số kỹ thuật',
        readonly=True
    )
    
    # ============ SỐ LƯỢNG VÀ GIÁ ============
    so_luong = fields.Integer(
        string='Số lượng',
        readonly=True
    )
    
    don_vi_tinh = fields.Char(
        string='Đơn vị tính',
        readonly=True
    )
    
    don_gia = fields.Float(
        string='Đơn giá',
        readonly=True
    )
    
    thanh_tien = fields.Float(
        string='Thành tiền',
        readonly=True
    )
    
    # ============ KHẤU HAO ============
    pp_khau_hao = fields.Selection([
        ('straight-line', 'Khấu hao tuyến tính'),
        ('degressive', 'Khấu hao giảm dần'),
        ('none', 'Không khấu hao')
    ], string='Phương pháp khấu hao', readonly=True)
    
    thoi_gian_su_dung = fields.Integer(
        string='Thời gian sử dụng (năm)',
        readonly=True
    )
    
    ty_le_khau_hao = fields.Float(
        string='Tỷ lệ khấu hao (%/năm)',
        readonly=True
    )
    
    # ============ NHÀ CUNG CẤP ============
    nha_cung_cap = fields.Char(
        string='Nhà cung cấp',
        readonly=True
    )
