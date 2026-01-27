# -*- coding: utf-8 -*-
# File tạm thời để xử lý migration - có thể xóa sau khi update thành công
from odoo import _, api, fields, models

class XacNhanTraWizardLine(models.TransientModel):
    """Wizard line tạm thời để xử lý migration"""
    _name = 'xac_nhan_tra_wizard_line'
    _description = 'Chi tiết xác nhận trả (tạm thời)'

    wizard_id = fields.Many2one('xac_nhan_tra_wizard', string='Wizard')
    name = fields.Char('Tên')


class XacNhanTraWizard(models.TransientModel):
    """Wizard tạm thời để xử lý migration"""
    _name = 'xac_nhan_tra_wizard'
    _description = 'Wizard xác nhận trả (tạm thời)'

    don_muon_id = fields.Many2one('don_muon_tai_san', string='Đơn mượn')
    line_ids = fields.One2many('xac_nhan_tra_wizard_line', 'wizard_id', string='Chi tiết')
    
    def action_confirm(self):
        """Xác nhận trả - chuyển hướng đến wizard mới"""
        if self.don_muon_id:
            return self.don_muon_id.action_xac_nhan_tra_hoan_tat()
        return {'type': 'ir.actions.act_window_close'}
