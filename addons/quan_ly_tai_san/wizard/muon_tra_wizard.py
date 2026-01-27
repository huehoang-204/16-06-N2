# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class DonMuonTuChoiWizard(models.TransientModel):
    """Wizard từ chối đơn mượn tài sản (dùng ở đơn đăng ký)"""
    _name = 'don_muon_tu_choi_wizard'
    _description = 'Wizard từ chối đơn mượn tài sản'
    
    don_muon_id = fields.Many2one(
        'don_muon_tai_san',
        string='Đơn mượn',
        required=True
    )
    ly_do = fields.Text('Lý do từ chối', required=True)
    
    def action_xac_nhan(self):
        """Xác nhận từ chối"""
        self.ensure_one()
        if not self.ly_do:
            raise UserError(_('Vui lòng nhập lý do từ chối!'))
        
        self.don_muon_id.action_xac_nhan_tu_choi(self.ly_do)
        return {'type': 'ir.actions.act_window_close'}


class MuonTraTuChoiWizard(models.TransientModel):
    """Wizard từ chối mượn trả tài sản (dùng ở quản lý mượn trả)"""
    _name = 'muon_tra_tu_choi_wizard'
    _description = 'Wizard từ chối mượn trả tài sản'
    
    muon_tra_id = fields.Many2one(
        'muon_tra_tai_san',
        string='Phiếu mượn trả',
        required=True
    )
    ly_do = fields.Text('Lý do từ chối', required=True)
    
    def action_xac_nhan(self):
        """Xác nhận từ chối"""
        self.ensure_one()
        if not self.ly_do:
            raise UserError(_('Vui lòng nhập lý do từ chối!'))
        
        self.muon_tra_id.action_xac_nhan_tu_choi(self.ly_do)
        return {'type': 'ir.actions.act_window_close'}


class MuonTraGiaHanWizard(models.TransientModel):
    """Wizard gia hạn thời gian trả"""
    _name = 'muon_tra_gia_han_wizard'
    _description = 'Wizard gia hạn thời gian trả'
    
    muon_tra_id = fields.Many2one(
        'muon_tra_tai_san',
        string='Phiếu mượn trả',
        required=True
    )
    thoi_gian_tra_moi = fields.Datetime(
        'Thời gian trả mới', 
        required=True
    )
    ly_do_gia_han = fields.Text('Lý do gia hạn', required=True)
    
    def action_xac_nhan(self):
        """Xác nhận gia hạn"""
        self.ensure_one()
        if not self.thoi_gian_tra_moi:
            raise UserError(_('Vui lòng chọn thời gian trả mới!'))
        if not self.ly_do_gia_han:
            raise UserError(_('Vui lòng nhập lý do gia hạn!'))
        
        if self.thoi_gian_tra_moi <= self.muon_tra_id.thoi_gian_tra_du_kien:
            raise UserError(_('Thời gian trả mới phải sau thời gian trả cũ!'))
        
        old_date = self.muon_tra_id.thoi_gian_tra_du_kien
        self.muon_tra_id.write({
            'thoi_gian_tra_du_kien': self.thoi_gian_tra_moi,
            'trang_thai': 'dang_muon',  # Đặt lại trạng thái nếu đang quá hạn
        })
        
        self.muon_tra_id.message_post(
            body=_('⏰ Đã gia hạn thời gian trả từ %s sang %s. Lý do: %s') % (
                old_date, 
                self.thoi_gian_tra_moi,
                self.ly_do_gia_han
            )
        )
        
        # Cập nhật đơn mượn gốc nếu có
        if self.muon_tra_id.ma_don_muon_id:
            self.muon_tra_id.ma_don_muon_id.write({
                'thoi_gian_tra': self.thoi_gian_tra_moi
            })
        
        return {'type': 'ir.actions.act_window_close'}


class MuonTraXacNhanTraWizard(models.TransientModel):
    """Wizard xác nhận trả tài sản với tình trạng"""
    _name = 'muon_tra_xac_nhan_tra_wizard'
    _description = 'Wizard xác nhận trả tài sản'
    
    muon_tra_id = fields.Many2one(
        'muon_tra_tai_san',
        string='Phiếu mượn trả',
        required=True
    )
    
    ghi_chu_chung = fields.Text('Ghi chú chung')
    
    line_ids = fields.One2many(
        'muon_tra_xac_nhan_tra_wizard_line',
        'wizard_id',
        string='Danh sách tài sản'
    )
    
    @api.model
    def default_get(self, fields_list):
        """Load dữ liệu mặc định từ phiếu mượn trả"""
        res = super().default_get(fields_list)
        if 'muon_tra_id' in res and res['muon_tra_id']:
            muon_tra = self.env['muon_tra_tai_san'].browse(res['muon_tra_id'])
            lines = []
            for line in muon_tra.muon_tra_line_ids:
                lines.append((0, 0, {
                    'muon_tra_line_id': line.id,
                    'phan_bo_tai_san_id': line.phan_bo_tai_san_id.id,
                    'tinh_trang_khi_tra': 'tot',
                }))
            res['line_ids'] = lines
        return res
    
    def action_xac_nhan(self):
        """Xác nhận trả tất cả tài sản"""
        self.ensure_one()
        
        # Cập nhật tình trạng từng tài sản vào muon_tra_line
        for line in self.line_ids:
            if line.muon_tra_line_id:
                line.muon_tra_line_id.write({
                    'tinh_trang_khi_tra': line.tinh_trang_khi_tra,
                    'ghi_chu_tra': line.ghi_chu,
                })
        
        # Gọi action hoàn tất trả
        self.muon_tra_id.action_xac_nhan_tra_hoan_tat()
        
        return {'type': 'ir.actions.act_window_close'}


class MuonTraXacNhanTraWizardLine(models.TransientModel):
    """Chi tiết từng tài sản trong wizard xác nhận trả"""
    _name = 'muon_tra_xac_nhan_tra_wizard_line'
    _description = 'Chi tiết tài sản xác nhận trả'
    
    wizard_id = fields.Many2one(
        'muon_tra_xac_nhan_tra_wizard',
        string='Wizard',
        required=True,
        ondelete='cascade'
    )
    
    muon_tra_line_id = fields.Many2one(
        'muon_tra_tai_san_line',
        string='Dòng mượn trả',
        required=True
    )
    
    phan_bo_tai_san_id = fields.Many2one(
        'phan_bo_tai_san',
        string='Tài sản',
        readonly=True
    )
    
    
    tinh_trang_khi_tra = fields.Selection([
        ('tot', 'Tốt'),
        ('binh_thuong', 'Bình thường'),
        ('hu_hong', 'Hư hỏng'),
        ('mat', 'Mất'),
    ], string='Tình trạng khi trả', required=True, default='tot')
    
    ghi_chu = fields.Text('Ghi chú tình trạng')

