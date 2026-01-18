from odoo import models, fields, api


class PhongBan(models.Model):
    _name = 'phong_ban'
    _description = 'Bảng chứa thông tin phòng ban'
    _rec_name = 'ten_phong_ban'

    ma_phong_ban = fields.Char("Mã phòng ban", required=True)
    ten_phong_ban = fields.Char("Tên phòng ban", required=True)
    
    # Computed field để tương thích với Odoo standard (name field)
    name = fields.Char("Tên", compute='_compute_name', store=True, readonly=True)
    
    lich_su_cong_tac_ids = fields.One2many("lich_su_cong_tac",string="Danh sách lịch sử công tác", inverse_name="phong_ban_id")
    
    @api.depends('ten_phong_ban')
    def _compute_name(self):
        """Compute name field from ten_phong_ban for Odoo compatibility"""
        for record in self:
            record.name = record.ten_phong_ban or ''

    # ids_van_ban_di = fields.One2many('van_ban_di', inverse_name='id_co_quan_ban_hanh', string="Văn bản đi")
