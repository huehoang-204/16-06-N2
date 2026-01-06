# models/wizard_sao_chep.py
from odoo import models, fields, api, _
from datetime import datetime


class BaoCaoTaiChinhWizard(models.TransientModel):
    _name = 'bao.cao.tai.chinh.wizard'
    _description = 'Wizard sao chép báo cáo tài chính'
    
    bao_cao_id = fields.Many2one('bao_cao_tai_chinh', string='Báo cáo nguồn', required=True)
    thang = fields.Integer(string='Tháng', required=True, default=lambda self: datetime.now().month)
    nam = fields.Integer(string='Năm', required=True, default=lambda self: datetime.now().year)
    ten_bao_cao_moi = fields.Char(string='Tên báo cáo mới', required=True)
    
    @api.model
    def default_get(self, fields):
        res = super(BaoCaoTaiChinhWizard, self).default_get(fields)
        if self.env.context.get('active_id'):
            bao_cao = self.env['bao_cao_tai_chinh'].browse(self.env.context['active_id'])
            res['bao_cao_id'] = bao_cao.id
            res['ten_bao_cao_moi'] = f"Sao chép của {bao_cao.name}"
        return res
    
    def action_sao_chep(self):
        """Sao chép báo cáo"""
        self.ensure_one()
        
        # Sao chép các giá trị
        values = {
            'name': self.ten_bao_cao_moi,
            'thang': self.thang,
            'nam': self.nam,
            'trang_thai': 'draft',
            'doanh_thu': self.bao_cao_id.doanh_thu,
            'chi_phi_khau_hao': self.bao_cao_id.chi_phi_khau_hao,
            'chi_phi_luong': self.bao_cao_id.chi_phi_luong,
            'chi_phi_van_phong': self.bao_cao_id.chi_phi_van_phong,
            'chi_phi_marketing': self.bao_cao_id.chi_phi_marketing,
            'chi_phi_dien_nuoc': self.bao_cao_id.chi_phi_dien_nuoc,
            'chi_phi_khac': self.bao_cao_id.chi_phi_khac,
        }
        
        # Tạo báo cáo mới
        bao_cao_moi = self.env['bao_cao_tai_chinh'].create(values)
        
        # Mở báo cáo mới
        return {
            'type': 'ir.actions.act_window',
            'name': 'Báo cáo mới',
            'res_model': 'bao_cao_tai_chinh',
            'res_id': bao_cao_moi.id,
            'view_mode': 'form',
            'target': 'current',
        }