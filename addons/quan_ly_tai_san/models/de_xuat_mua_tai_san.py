# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, MissingError
from datetime import date

_logger = logging.getLogger(__name__)

class DeXuatMuaTaiSan(models.Model):
    """
    Model đề xuất mua tài sản - Bước 1 trong luồng mua thiết bị
    
    QUY TRÌNH:
    1. Tạo đề xuất mua tài sản (module quan_ly_tai_san)
    2. Gửi đề xuất → Tự động tạo đơn phê duyệt ở module tài chính
    3. Phê duyệt đơn chỉ được thực hiện tại module quan_ly_tai_chinh
    
    LƯU Ý QUAN TRỌNG:
    - Module này CHỈ cho phép TẠO và GỬI đề xuất
    - KHÔNG được phép tự phê duyệt đề xuất tại module này
    - Phê duyệt PHẢI thực hiện tại module quan_ly_tai_chinh
    - Các callback _on_approval_* chỉ được gọi từ module tài chính
    """
    _name = 'de_xuat_mua_tai_san'
    _description = 'Đề xuất mua tài sản'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'ma_de_xuat'
    _order = 'ngay_de_xuat desc'

    # ============ THÔNG TIN CƠ BẢN ============
    ma_de_xuat = fields.Char(
        string='Mã đề xuất',
        required=True,
        readonly=True,
        copy=False,
        default='New',
        tracking=True,
        help='Mã tự động tạo khi lưu đề xuất'
    )
    
    ten_de_xuat = fields.Char(
        string='Tiêu đề đề xuất',
        required=True,
        tracking=True,
        help='Tiêu đề mô tả ngắn gọn về đề xuất mua'
    )
    
    ngay_de_xuat = fields.Date(
        string='Ngày đề xuất',
        default=fields.Date.context_today,
        required=True,
        tracking=True
    )
    
    nguoi_de_xuat_id = fields.Many2one(
        'res.users',
        string='Người đề xuất',
        default=lambda self: self.env.user,
        required=False,
        tracking=True,
        ondelete='set null'
    )
    
    phong_ban_id = fields.Many2one(
        'phong_ban',
        string='Phòng ban',
        required=False,
        ondelete='set null',
        tracking=True,
        help='Phòng ban đề xuất mua thiết bị'
    )
    
    # ============ CHI TIẾT ĐỀ XUẤT ============
    line_ids = fields.One2many(
        'de_xuat_mua_tai_san.line',
        'de_xuat_id',
        string='Chi tiết thiết bị',
        required=True,
        help='Danh sách thiết bị cần mua'
    )
    
    # ============ TỔNG TIỀN ============
    tong_gia_tri = fields.Float(
        string='Tổng giá trị',
        compute='_compute_tong_gia_tri',
        store=True,
        tracking=True,
        help='Tổng giá trị tất cả thiết bị trong đề xuất'
    )
    
    don_vi_tien_te = fields.Selection([
        ('vnd', 'VNĐ'),
        ('usd', 'USD'),
    ], string='Đơn vị tiền tệ', default='vnd', required=True)
    
    # ============ LÝ DO VÀ MÔ TẢ ============
    ly_do = fields.Text(
        string='Lý do đề xuất',
        required=True,
        tracking=True,
        help='Giải thích lý do cần mua các thiết bị này'
    )
    
    mo_ta = fields.Html(
        string='Mô tả chi tiết',
        tracking=True,
        help='Mô tả chi tiết về đề xuất'
    )
    
    # ============ FILE ĐÍNH KÈM ============
    dinh_kem_ids = fields.Many2many(
        'ir.attachment',
        string='File đính kèm',
        help='File báo giá, hình ảnh, tài liệu kỹ thuật,...'
    )
    
    # ============ TRẠNG THÁI ============
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('submitted', 'Đã gửi'),
        ('waiting_approval', 'Chờ phê duyệt tài chính'),
        ('approved', 'Đã phê duyệt'),
        ('rejected', 'Từ chối'),
        ('cancelled', 'Đã hủy'),
    ], string='Trạng thái', default='draft', required=True, tracking=True)
    
    # ============ NGÀY DỰ KIẾN ============
    ngay_du_kien_nhan = fields.Date(
        string='Ngày dự kiến nhận hàng',
        tracking=True,
        help='Ngày dự kiến nhận được thiết bị'
    )
    
    # ============ LIÊN KẾT ĐƠN PHÊ DUYỆT ============
    phe_duyet_id = fields.Many2one(
        'phe_duyet_mua_tai_san',
        string='Đơn phê duyệt',
        readonly=True,
        tracking=True,
        ondelete='set null',
        help='Đơn phê duyệt được tạo tự động ở module tài chính'
    )
    
    # ============ LIÊN KẾT TÀI SẢN ĐÃ TẠO ============
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
    
    # ============ GHI CHÚ ============
    ghi_chu = fields.Text(
        string='Ghi chú',
        tracking=True
    )
    
    # ============ COMPUTE METHODS ============
    @api.depends('tai_san_ids')
    def _compute_tai_san_count(self):
        for record in self:
            record.tai_san_count = len(record.tai_san_ids)
    
    @api.depends('line_ids.thanh_tien')
    def _compute_tong_gia_tri(self):
        for record in self:
            record.tong_gia_tri = sum(record.line_ids.mapped('thanh_tien'))
    
    # ============ CRUD METHODS ============
    @api.model
    def create(self, vals):
        if vals.get('ma_de_xuat', 'New') == 'New':
            vals['ma_de_xuat'] = self.env['ir.sequence'].next_by_code('de_xuat_mua_tai_san') or 'New'
        return super(DeXuatMuaTaiSan, self).create(vals)
    
    # ============ ACTION METHODS ============
    def action_submit(self):
        """Gửi đề xuất và tự động tạo đơn phê duyệt ở module tài chính"""
        for record in self:
            if not record.line_ids:
                raise UserError(_('Vui lòng thêm ít nhất một thiết bị vào đề xuất.'))
            
            # Kiểm tra tất cả line đều phải có danh_muc_ts_id
            for line in record.line_ids:
                if not line.danh_muc_ts_id:
                    raise UserError(_(
                        'Vui lòng chọn danh mục tài sản cho thiết bị: %s'
                    ) % (line.ten_thiet_bi or _('(Chưa đặt tên)')))
            
            if record.tong_gia_tri <= 0:
                raise UserError(_('Tổng giá trị phải lớn hơn 0.'))
            
            # Chuyển trạng thái
            record.state = 'submitted'
            
            # Tự động tạo đơn phê duyệt ở module tài chính
            record._create_approval_request()
            
            # Chuyển sang trạng thái chờ phê duyệt
            record.state = 'waiting_approval'
            
            # Gửi thông báo
            record.message_post(
                body=_('Đề xuất đã được gửi và tạo đơn phê duyệt tài chính.'),
                subject=_('Đề xuất đã gửi')
            )
    
    def _create_approval_request(self):
        """Tạo đơn phê duyệt tự động ở module tài chính"""
        self.ensure_one()
        
        # Kiểm tra module tài chính đã cài đặt chưa
        if not self.env['ir.module.module'].search([
            ('name', '=', 'quan_ly_tai_chinh'), 
            ('state', '=', 'installed')
        ]):
            raise UserError(_('Module Quản lý tài chính chưa được cài đặt.'))
        
        # Tạo đơn phê duyệt
        phe_duyet_obj = self.env['phe_duyet_mua_tai_san']
        
        # Thu thập chi tiết từ line_ids - XỬ LÝ AN TOÀN
        line_vals = []
        for line in self.line_ids:
            # Kiểm tra và xử lý an toàn danh_muc_ts_id
            danh_muc_id = False
            if line.danh_muc_ts_id:
                try:
                    # Đảm bảo record tồn tại và có ID hợp lệ
                    if hasattr(line.danh_muc_ts_id, 'id') and line.danh_muc_ts_id.id:
                        # Kiểm tra exists() để đảm bảo record thực sự tồn tại trong DB
                        if line.danh_muc_ts_id.exists():
                            danh_muc_id = line.danh_muc_ts_id.id
                except Exception:
                    # Nếu có bất kỳ lỗi nào, bỏ qua và để False
                    danh_muc_id = False
            
            # Nếu vẫn chưa có danh_muc_id thì raise error
            if not danh_muc_id:
                raise UserError(_(
                    'Không thể tạo đơn phê duyệt: Thiết bị "%s" chưa có danh mục tài sản hợp lệ.'
                ) % (line.ten_thiet_bi or _('(Chưa đặt tên)')))
            
            line_data = {
                'ten_thiet_bi': line.ten_thiet_bi or '',
                'danh_muc_ts_id': danh_muc_id,
                'mo_ta': line.mo_ta or '',
                'thong_so_ky_thuat': line.thong_so_ky_thuat or '',
                'so_luong': line.so_luong or 1,
                'don_vi_tinh': line.don_vi_tinh or '',
                'don_gia': line.don_gia or 0.0,
                'thanh_tien': line.thanh_tien or 0.0,
                'pp_khau_hao': line.pp_khau_hao or 'straight-line',
                'thoi_gian_su_dung': line.thoi_gian_su_dung or 0,
                'ty_le_khau_hao': line.ty_le_khau_hao or 0.0,
                'nha_cung_cap': line.nha_cung_cap or '',
            }
            line_vals.append((0, 0, line_data))
        
        # Xử lý an toàn các trường Many2one
        nguoi_de_xuat_id = False
        if self.nguoi_de_xuat_id and self.nguoi_de_xuat_id.exists():
            nguoi_de_xuat_id = self.nguoi_de_xuat_id.id
        
        phong_ban_id = False
        if self.phong_ban_id and self.phong_ban_id.exists():
            phong_ban_id = self.phong_ban_id.id
        
        phe_duyet_vals = {
            'de_xuat_mua_id': self.id,
            'ten_de_xuat': self.ten_de_xuat or '',
            'ngay_de_xuat': self.ngay_de_xuat or fields.Date.today(),
            'nguoi_de_xuat_id': nguoi_de_xuat_id,
            'phong_ban_id': phong_ban_id,
            'tong_gia_tri': self.tong_gia_tri or 0.0,
            'don_vi_tien_te': self.don_vi_tien_te or 'vnd',
            'ly_do': self.ly_do or '',
            'mo_ta': self.mo_ta or '',
            'ngay_du_kien_nhan': self.ngay_du_kien_nhan or False,
            'line_ids': line_vals,
        }
        
        phe_duyet = phe_duyet_obj.create(phe_duyet_vals)
        self.phe_duyet_id = phe_duyet.id
        
        # Tạo activity cho người có quyền phê duyệt tài chính
        try:
            finance_users = self.env.ref('quan_ly_tai_chinh.group_finance_manager').users
            if finance_users:
                phe_duyet.activity_schedule(
                    'mail.mail_activity_data_todo',
                    user_id=finance_users[0].id,
                    summary=f'Phê duyệt đề xuất mua tài sản: {self.ma_de_xuat}'
                )
        except:
            # Bỏ qua nếu không tìm thấy group hoặc không tạo được activity
            pass
        
        return phe_duyet
    
    def action_cancel(self):
        """Hủy đề xuất"""
        for record in self:
            if record.state in ['approved']:
                raise UserError(_('Không thể hủy đề xuất đã được phê duyệt.'))
            
            # Hủy đơn phê duyệt nếu có
            if record.phe_duyet_id and record.phe_duyet_id.state == 'draft':
                record.phe_duyet_id.action_cancel()
            
            record.state = 'cancelled'
    
    def action_reset_to_draft(self):
        """Đưa về nháp"""
        for record in self:
            if record.state not in ['rejected', 'cancelled']:
                raise UserError(_('Chỉ có thể đưa về nháp các đề xuất bị từ chối hoặc đã hủy.'))
            record.state = 'draft'
    
    def action_view_approval(self):
        """Xem đơn phê duyệt"""
        self.ensure_one()
        if not self.phe_duyet_id:
            raise UserError(_('Chưa có đơn phê duyệt nào được tạo.'))
        
        return {
            'name': _('Đơn phê duyệt mua tài sản'),
            'type': 'ir.actions.act_window',
            'res_model': 'phe_duyet_mua_tai_san',
            'view_mode': 'form',
            'res_id': self.phe_duyet_id.id if self.phe_duyet_id else False,
            'target': 'current',
        }
    
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
    
    # ============ CONSTRAINTS ============
    @api.constrains('state')
    def _check_state_transition(self):
        """
        Ngăn chặn việc thay đổi trạng thái trực tiếp sang approved/rejected
        Chỉ cho phép thay đổi thông qua các method được định nghĩa
        """
        for record in self:
            # Kiểm tra xem có đang cố gắng thay đổi trạng thái trực tiếp không
            # Chỉ cho phép draft, submitted, waiting_approval, cancelled
            # approved và rejected chỉ được set thông qua callback từ module tài chính
            if record.state in ['approved', 'rejected']:
                # Kiểm tra xem có đang trong context của callback không
                if not self.env.context.get('from_finance_approval'):
                    # Cho phép nếu đang trong quá trình create/write từ database
                    if not self.env.context.get('_bypass_state_check'):
                        pass  # Cho phép vì có thể đang load từ database
    
    # ============ WRITE METHOD - Override để bảo vệ ============
    def write(self, vals):
        """
        Override write để ngăn chặn việc thay đổi trạng thái không hợp lệ
        """
        # Nếu đang cố gắng thay đổi state sang approved/rejected mà không phải từ callback
        if 'state' in vals and vals['state'] in ['approved', 'rejected']:
            if not self.env.context.get('from_finance_approval'):
                # Kiểm tra xem method nào đang gọi
                import inspect
                caller_method = inspect.stack()[1].function
                # Chỉ cho phép từ callback methods
                if caller_method not in ['_on_approval_approved', '_on_approval_rejected']:
                    raise UserError(_(
                        'KHÔNG THỂ TỰ PHÊ DUYỆT ĐỀ XUẤT!\n\n'
                        'Đề xuất mua tài sản chỉ có thể được phê duyệt thông qua '
                        'module Quản lý Tài chính.\n\n'
                        'Vui lòng truy cập menu: Tài chính > Phê duyệt mua tài sản '
                        'để thực hiện phê duyệt.'
                    ))
        
        return super(DeXuatMuaTaiSan, self).write(vals)
    
    # ============ CALLBACK METHODS - Chỉ được gọi từ module tài chính ============
    def _on_approval_approved(self):
        """
        Callback khi đơn phê duyệt được duyệt
        LƯU Ý: Method này CHỈ được gọi từ module quan_ly_tai_chinh
        """
        self.ensure_one()
        # Set context để bypass constraint check
        self.with_context(from_finance_approval=True).write({
            'state': 'approved'
        })
        self.message_post(
            body=_('Đề xuất đã được phê duyệt bởi bộ phận tài chính.'),
            subject=_('Đề xuất đã phê duyệt')
        )
    
    def _on_approval_rejected(self):
        """
        Callback khi đơn phê duyệt bị từ chối
        LƯU Ý: Method này CHỈ được gọi từ module quan_ly_tai_chinh
        """
        self.ensure_one()
        # Set context để bypass constraint check
        self.with_context(from_finance_approval=True).write({
            'state': 'rejected'
        })
        self.message_post(
            body=_('Đề xuất đã bị từ chối bởi bộ phận tài chính.'),
            subject=_('Đề xuất bị từ chối')
        )
    
    def _on_approval_deleted(self):
        """
        Callback khi đơn phê duyệt bị xóa ở module tài chính
        Reset trạng thái về draft để có thể xóa
        """
        self.ensure_one()
        try:
            # Reset trạng thái về draft để có thể xóa
            self.with_context(from_finance_approval=True).write({
                'state': 'draft',
                'phe_duyet_id': False
            })
            self.message_post(
                body=_('Đơn phê duyệt đã bị xóa. Đề xuất trở về trạng thái nháp.'),
                subject=_('Đơn phê duyệt bị xóa')
            )
        except Exception as e:
            _logger.warning(f"Could not reset de_xuat_mua_tai_san {self.id}: {e}")
    
    def action_reset_to_draft(self):
        """
        Action button để reset trạng thái từ approved/rejected/done về draft
        Sử dụng khi approval bị xóa nhưng proposal vẫn còn ở trạng thái approved
        """
        for record in self:
            if record.state in ('approved', 'rejected', 'done'):
                record.with_context(force_reset=True).write({
                    'state': 'draft',
                    'phe_duyet_id': False,
                })
                record.message_post(
                    body=_('Trạng thái đã được reset về nháp để có thể xóa.'),
                    subject=_('Reset trạng thái')
                )
        return True


class DeXuatMuaTaiSanLine(models.Model):
    """Chi tiết đề xuất mua tài sản"""
    _name = 'de_xuat_mua_tai_san.line'
    _description = 'Chi tiết đề xuất mua tài sản'
    _order = 'sequence, id'
    
    def _auto_init(self):
        """Override _auto_init để cleanup dữ liệu cũ khi module load"""
        res = super(DeXuatMuaTaiSanLine, self)._auto_init()
        # Cleanup invalid danh_muc_ts_id after table is created
        try:
            self.env.cr.execute("""
                UPDATE de_xuat_mua_tai_san_line
                SET danh_muc_ts_id = NULL
                WHERE danh_muc_ts_id IS NOT NULL
                  AND danh_muc_ts_id NOT IN (SELECT id FROM danh_muc_tai_san)
            """)
            _logger.info("Cleaned up invalid danh_muc_ts_id references")
        except Exception as e:
            _logger.warning(f"Could not cleanup invalid danh_muc_ts_id: {e}")
        return res
    
    sequence = fields.Integer(string='STT', default=10)
    
    de_xuat_id = fields.Many2one(
        'de_xuat_mua_tai_san',
        string='Đề xuất',
        required=True,
        ondelete='cascade',
        index=True
    )
    
    # ============ THÔNG TIN THIẾT BỊ ============
    ten_thiet_bi = fields.Char(
        string='Tên thiết bị',
        required=True
    )
    
    danh_muc_ts_id = fields.Many2one(
        'danh_muc_tai_san',
        string='Danh mục tài sản',
        required=False,
        ondelete='set null',
        help='Danh mục tài sản để phân loại thiết bị'
    )
    
    # ============ OVERRIDE __GETATTRIBUTE__ ĐỂ BẮT LỖI SỚM ============
    def __getattribute__(self, name):
        """Override để bắt lỗi khi access danh_muc_ts_id không hợp lệ"""
        try:
            value = super(DeXuatMuaTaiSanLine, self).__getattribute__(name)
            # Nếu là danh_muc_ts_id và là recordset
            if name == 'danh_muc_ts_id' and value and hasattr(value, '_name'):
                # Kiểm tra xem record có tồn tại không
                if value and not value.exists():
                    # Set về False trong database
                    try:
                        self.env.cr.execute(
                            "UPDATE de_xuat_mua_tai_san_line SET danh_muc_ts_id = NULL WHERE id = %s",
                            (self.id,)
                        )
                        self.env.cache.invalidate()
                    except:
                        pass
                    return self.env['danh_muc_tai_san']
            return value
        except (AttributeError, MissingError):
            if name == 'danh_muc_ts_id':
                return self.env['danh_muc_tai_san']
            raise
    
    mo_ta = fields.Text(
        string='Mô tả',
        help='Mô tả ngắn về thiết bị'
    )
    
    thong_so_ky_thuat = fields.Text(
        string='Thông số kỹ thuật',
        help='Thông số kỹ thuật chi tiết của thiết bị'
    )
    
    # ============ SỐ LƯỢNG VÀ GIÁ ============
    so_luong = fields.Integer(
        string='Số lượng',
        default=1,
        required=True
    )
    
    don_vi_tinh = fields.Char(
        string='Đơn vị tính',
        default='Chiếc',
        required=True
    )
    
    don_gia = fields.Float(
        string='Đơn giá',
        required=True
    )
    
    thanh_tien = fields.Float(
        string='Thành tiền',
        compute='_compute_thanh_tien',
        store=True
    )
    
    # ============ KHẤU HAO ============
    pp_khau_hao = fields.Selection([
        ('straight-line', 'Khấu hao tuyến tính'),
        ('degressive', 'Khấu hao giảm dần'),
        ('none', 'Không khấu hao')
    ], string='Phương pháp khấu hao', default='straight-line', required=True)
    
    thoi_gian_su_dung = fields.Integer(
        string='Thời gian sử dụng (năm)',
        default=5,
        help='Thời gian sử dụng dự kiến của thiết bị'
    )
    
    ty_le_khau_hao = fields.Float(
        string='Tỷ lệ khấu hao (%/năm)',
        compute='_compute_ty_le_khau_hao',
        store=True,
        readonly=False,  # Cho phép edit thủ công
        help='Tỷ lệ khấu hao hàng năm (tự động tính = 100 / thời gian sử dụng)'
    )
    
    # ============ NHÀ CUNG CẤP ============
    nha_cung_cap = fields.Char(
        string='Nhà cung cấp đề xuất',
        help='Nhà cung cấp được đề xuất mua thiết bị'
    )
    
    # ============ COMPUTE METHODS ============
    @api.depends('so_luong', 'don_gia')
    def _compute_thanh_tien(self):
        for record in self:
            record.thanh_tien = record.so_luong * record.don_gia
    
    @api.depends('thoi_gian_su_dung')
    def _compute_ty_le_khau_hao(self):
        """Tự động tính tỷ lệ khấu hao dựa trên thời gian sử dụng"""
        for record in self:
            if record.thoi_gian_su_dung and record.thoi_gian_su_dung > 0:
                record.ty_le_khau_hao = 100.0 / record.thoi_gian_su_dung
            else:
                record.ty_le_khau_hao = 0.0
    
    # ============ ONCHANGE METHODS ============
    @api.onchange('danh_muc_ts_id')
    def _onchange_danh_muc_ts_id(self):
        """Xử lý an toàn khi danh_muc_ts_id thay đổi hoặc không hợp lệ"""
        for record in self:
            if record.danh_muc_ts_id:
                try:
                    # Kiểm tra xem record có tồn tại không
                    if not record.danh_muc_ts_id.exists():
                        record.danh_muc_ts_id = False
                except Exception:
                    record.danh_muc_ts_id = False
    
    # ============ CONSTRAINTS ============
    @api.constrains('so_luong', 'don_gia', 'thoi_gian_su_dung', 'ty_le_khau_hao')
    def _check_positive_values(self):
        for record in self:
            if record.so_luong <= 0:
                raise ValidationError(_('Số lượng phải lớn hơn 0.'))
            if record.don_gia < 0:
                raise ValidationError(_('Đơn giá không thể âm.'))
            if record.pp_khau_hao != 'none':
                if record.thoi_gian_su_dung <= 0:
                    raise ValidationError(_('Thời gian sử dụng phải lớn hơn 0 nếu có khấu hao.'))
                if record.ty_le_khau_hao <= 0 or record.ty_le_khau_hao > 100:
                    raise ValidationError(_('Tỷ lệ khấu hao phải trong khoảng 0-100%.'))
    
    # ============ OVERRIDE READ METHOD ============
    def read(self, fields=None, load='_classic_read'):
        """Override read để xử lý an toàn danh_muc_ts_id không hợp lệ"""
        try:
            result = super(DeXuatMuaTaiSanLine, self).read(fields=fields, load=load)
            return result
        except AttributeError as e:
            # Nếu gặp lỗi AttributeError (thường là do Many2one không hợp lệ)
            # Tự động clean up và đọc lại
            _logger.warning(f"Cleaning up invalid danh_muc_ts_id in line {self.ids}: {e}")
            for record in self:
                try:
                    if record.danh_muc_ts_id and not record.danh_muc_ts_id.exists():
                        record.with_context(skip_onchange=True).sudo().write({'danh_muc_ts_id': False})
                except Exception:
                    record.with_context(skip_onchange=True).sudo().write({'danh_muc_ts_id': False})
            # Thử đọc lại
            return super(DeXuatMuaTaiSanLine, self).read(fields=fields, load=load)
    
    # ============ UTILITY METHODS ============
    @api.model
    def _cleanup_invalid_danh_muc(self):
        """
        Method tiện ích để dọc dữ liệu cũ có danh_muc_ts_id không hợp lệ
        Chạy thủ công nếu cần: self.env['de_xuat_mua_tai_san.line']._cleanup_invalid_danh_muc()
        """
        lines = self.search([])
        cleaned = 0
        for line in lines:
            try:
                if line.danh_muc_ts_id:
                    if not line.danh_muc_ts_id.exists():
                        line.with_context(skip_onchange=True).write({'danh_muc_ts_id': False})
                        cleaned += 1
            except Exception:
                line.with_context(skip_onchange=True).write({'danh_muc_ts_id': False})
                cleaned += 1
        return cleaned
