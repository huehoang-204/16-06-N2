from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class DonMuonTaiSanLine(models.Model):
    _name = 'don_muon_tai_san_line'
    _description = 'Chi tiết đơn mượn tài sản'

    don_muon_id = fields.Many2one('don_muon_tai_san', string='Mã đơn mượn', ondelete='cascade')
    phan_bo_tai_san_id = fields.Many2one('phan_bo_tai_san', string='Tài sản', required=True, ondelete='cascade')
    so_luong = fields.Integer('Số lượng', default=1, readonly=True)
    ghi_chu = fields.Char('Ghi chú', default='')
    
    # ============ TÌNH TRẠNG TÀI SẢN ============
    tinh_trang_truoc_muon = fields.Selection([
        ('tot', 'Tốt'),
        ('binh_thuong', 'Bình thường'),
        ('cu', 'Cũ'),
        ('hu_hong_nhe', 'Hư hỏng nhẹ'),
    ], string='Tình trạng trước khi mượn', default='tot',
       help='Ghi nhận tình trạng tài sản trước khi cho mượn')
    
    tinh_trang_sau_tra = fields.Selection([
        ('tot', 'Tốt'),
        ('binh_thuong', 'Bình thường'),
        ('hu_hong', 'Hư hỏng'),
        ('mat', 'Mất'),
    ], string='Tình trạng sau khi trả',
       help='Ghi nhận tình trạng tài sản sau khi được trả')
    
    ghi_chu_tinh_trang = fields.Text('Ghi chú tình trạng',
       help='Mô tả chi tiết tình trạng tài sản nếu có hư hỏng hoặc vấn đề')
    
    # ============ THỜI GIAN MƯỢN/TRẢ THỰC TẾ ============
    thoi_gian_cho_muon = fields.Datetime('Thời gian cho mượn thực tế',
       help='Thời điểm thực tế tài sản được giao cho người mượn', readonly=True)
    
    thoi_gian_tra_thuc_te = fields.Datetime('Thời gian trả thực tế',
       help='Thời điểm thực tế người mượn trả lại tài sản', readonly=True)
    
    nguoi_giao_id = fields.Many2one('res.users', string='Người giao',
       readonly=True, help='Người thực hiện giao tài sản')
    
    nguoi_nhan_tra_id = fields.Many2one('res.users', string='Người nhận trả',
       readonly=True, help='Người xác nhận nhận lại tài sản')
    
    # ============ TRẠNG THÁI DÒNG ============
    trang_thai_line = fields.Selection([
        ('cho_muon', 'Chờ mượn'),
        ('dang_muon', 'Đang mượn'),
        ('da_tra', 'Đã trả'),
        ('hong', 'Bị hỏng'),
        ('mat', 'Bị mất'),
    ], string='Trạng thái', default='cho_muon', tracking=True)
