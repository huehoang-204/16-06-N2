from odoo import models, fields, api
from odoo.exceptions import UserError, AccessDenied
import hashlib


class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ho_ten'

    ma_dinh_danh = fields.Char("Mã định danh", required=True)
    ho_ten = fields.Char("Họ tên", required=True, default='')
    ngay_sinh = fields.Date("Ngày sinh")
    que_quan = fields.Char("Quê quán")
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại")
    lich_su_cong_tac_ids = fields.One2many("lich_su_cong_tac", string="Danh sách lịch sử công tác", inverse_name="nhan_vien_id")
    tuoi = fields.Integer("Tuổi", compute="_compute_tuoi", store=True)
    
    # Liên kết với User Odoo (nếu có)
    user_id = fields.Many2one('res.users', string='Tài khoản Odoo', ondelete='set null')
    
    # Thông tin đăng nhập riêng cho web app bên ngoài
    web_username = fields.Char("Tên đăng nhập web")
    web_password_hash = fields.Char("Mật khẩu (hash)")
    is_web_active = fields.Boolean("Kích hoạt web", default=False)
    last_login = fields.Datetime("Đăng nhập lần cuối")

    @api.depends('ngay_sinh')
    def _compute_tuoi(self):
        for record in self:
            if record.ngay_sinh:
                record.tuoi = (fields.Date.today() - record.ngay_sinh).days // 365

    def _hash_password(self, password):
        """Hash mật khẩu sử dụng SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()

    @api.model
    def web_register(self, data):
        """
        Đăng ký tài khoản web mới
        Args:
            data: dict với keys: ma_dinh_danh, ho_ten, email, so_dien_thoai, username, password
        Returns:
            dict: {success: bool, message: str, employee_id: int}
        """
        try:
            # Kiểm tra username đã tồn tại chưa
            existing = self.sudo().search([('web_username', '=', data.get('username'))], limit=1)
            if existing:
                return {'success': False, 'message': 'Tên đăng nhập đã tồn tại'}
            
            # Kiểm tra mã định danh đã tồn tại chưa
            existing_employee = self.sudo().search([('ma_dinh_danh', '=', data.get('ma_dinh_danh'))], limit=1)
            if existing_employee:
                return {'success': False, 'message': 'Mã định danh đã tồn tại'}
            
            # Tạo nhân viên mới
            employee = self.sudo().create({
                'ma_dinh_danh': data.get('ma_dinh_danh'),
                'ho_ten': data.get('ho_ten'),
                'email': data.get('email'),
                'so_dien_thoai': data.get('so_dien_thoai'),
                'web_username': data.get('username'),
                'web_password_hash': self._hash_password(data.get('password', '')),
                'is_web_active': True,
            })
            
            return {
                'success': True,
                'message': 'Đăng ký thành công',
                'employee_id': employee.id,
                'employee': {
                    'id': employee.id,
                    'ma_dinh_danh': employee.ma_dinh_danh,
                    'ho_ten': employee.ho_ten,
                    'email': employee.email,
                }
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @api.model
    def web_login(self, username, password):
        """
        Đăng nhập cho web app bên ngoài
        Args:
            username: tên đăng nhập
            password: mật khẩu (chưa hash)
        Returns:
            dict: {success: bool, message: str, employee: dict}
        """
        try:
            password_hash = self._hash_password(password)
            employee = self.sudo().search([
                ('web_username', '=', username),
                ('web_password_hash', '=', password_hash),
                ('is_web_active', '=', True)
            ], limit=1)
            
            if not employee:
                return {'success': False, 'message': 'Tên đăng nhập hoặc mật khẩu không đúng'}
            
            # Cập nhật thời gian đăng nhập
            employee.sudo().write({'last_login': fields.Datetime.now()})
            
            return {
                'success': True,
                'message': 'Đăng nhập thành công',
                'employee': {
                    'id': employee.id,
                    'ma_dinh_danh': employee.ma_dinh_danh,
                    'ho_ten': employee.ho_ten,
                    'email': employee.email,
                    'so_dien_thoai': employee.so_dien_thoai,
                    'tuoi': employee.tuoi,
                }
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @api.model
    def web_change_password(self, username, old_password, new_password):
        """Đổi mật khẩu"""
        try:
            old_hash = self._hash_password(old_password)
            employee = self.sudo().search([
                ('web_username', '=', username),
                ('web_password_hash', '=', old_hash),
            ], limit=1)
            
            if not employee:
                return {'success': False, 'message': 'Mật khẩu cũ không đúng'}
            
            employee.sudo().write({
                'web_password_hash': self._hash_password(new_password)
            })
            
            return {'success': True, 'message': 'Đổi mật khẩu thành công'}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @api.model
    def get_employee_by_username(self, username):
        """Lấy thông tin nhân viên theo username"""
        employee = self.sudo().search([('web_username', '=', username)], limit=1)
        if not employee:
            return {'success': False, 'message': 'Không tìm thấy nhân viên'}
        
        return {
            'success': True,
            'employee': {
                'id': employee.id,
                'ma_dinh_danh': employee.ma_dinh_danh,
                'ho_ten': employee.ho_ten,
                'email': employee.email,
                'so_dien_thoai': employee.so_dien_thoai,
                'tuoi': employee.tuoi,
                'last_login': employee.last_login.isoformat() if employee.last_login else None,
            }
        }
