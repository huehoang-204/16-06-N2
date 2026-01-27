# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
import json
import logging

_logger = logging.getLogger(__name__)


class DashboardMain(models.TransientModel):
    """Dashboard Tổng quan - Transient Model để luôn tính toán mới"""
    _name = 'dashboard.main'
    _description = 'Dashboard Tổng quan'

    name = fields.Char('Tên', default='Dashboard', readonly=True)
    
    # Stats fields - computed
    total_tai_san = fields.Integer('Tổng tài sản', compute='_compute_stats', store=False)
    active_tai_san = fields.Integer('Đang sử dụng', compute='_compute_stats', store=False)
    dang_muon = fields.Integer('Đang cho mượn', compute='_compute_stats', store=False)
    don_cho_duyet = fields.Integer('Đơn chờ duyệt', compute='_compute_stats', store=False)
    qua_han = fields.Integer('Quá hạn', compute='_compute_stats', store=False)
    total_value = fields.Float('Tổng giá trị', compute='_compute_stats', store=False)
    currency_id = fields.Many2one('res.currency', compute='_compute_currency')
    
    # HTML fields for display
    thong_bao_html = fields.Html('Thông báo', compute='_compute_thong_bao_html', sanitize=False)
    hoat_dong_html = fields.Html('Hoạt động', compute='_compute_hoat_dong_html', sanitize=False)

    @api.model
    def default_get(self, fields_list):
        """Override để tính toán dữ liệu dashboard ngay khi mở form"""
        res = super().default_get(fields_list)
        
        # Tính toán dữ liệu dashboard
        TaiSan = self.env['tai_san']
        
        # Tổng tài sản
        if 'total_tai_san' in fields_list:
            res['total_tai_san'] = TaiSan.search_count([])
        
        # Tài sản đang sử dụng = chưa thanh lý
        if 'active_tai_san' in fields_list:
            res['active_tai_san'] = TaiSan.search_count([
                ('trang_thai_thanh_ly', 'in', ['da_phan_bo', 'chua_phan_bo', 'chua_thanh_ly'])
            ])
        
        # Tổng giá trị
        if 'total_value' in fields_list:
            tai_san_list = TaiSan.search([])
            res['total_value'] = sum(
                ts.gia_tri_hien_tai or ts.gia_tri_ban_dau or 0 
                for ts in tai_san_list
            )
        
        # Thống kê mượn trả
        try:
            DonMuon = self.env['don_muon_tai_san']
            if 'don_cho_duyet' in fields_list:
                res['don_cho_duyet'] = DonMuon.search_count([('trang_thai', '=', 'cho_duyet')])
            if 'dang_muon' in fields_list:
                res['dang_muon'] = DonMuon.search_count([('trang_thai', '=', 'da_duyet')])
            
            # Quá hạn
            MuonTra = self.env['muon_tra_tai_san']
            if 'qua_han' in fields_list:
                res['qua_han'] = MuonTra.search_count([
                    ('trang_thai', '=', 'dang_muon'),
                    ('thoi_gian_tra_du_kien', '<', fields.Datetime.now())
                ])
        except Exception as e:
            _logger.warning(f"Error computing muon_tra stats in default_get: {e}")
            if 'don_cho_duyet' in fields_list:
                res['don_cho_duyet'] = 0
            if 'dang_muon' in fields_list:
                res['dang_muon'] = 0
            if 'qua_han' in fields_list:
                res['qua_han'] = 0
        
        # Tính toán thông báo HTML
        if 'thong_bao_html' in fields_list:
            notifications = []
            don_cho = res.get('don_cho_duyet', 0)
            qua_han_count = res.get('qua_han', 0)
            
            if don_cho > 0:
                notifications.append({
                    'icon': 'fa-clock-o',
                    'color': 'warning',
                    'message': f'{don_cho} đơn mượn đang chờ duyệt',
                })
            if qua_han_count > 0:
                notifications.append({
                    'icon': 'fa-exclamation-triangle',
                    'color': 'danger',
                    'message': f'{qua_han_count} tài sản quá hạn chưa trả',
                })
            
            # Thêm phê duyệt mua
            try:
                PheDuyet = self.env['phe_duyet_mua_tai_san']
                phe_duyet_cho = PheDuyet.search_count([('state', '=', 'draft')])
                if phe_duyet_cho > 0:
                    notifications.append({
                        'icon': 'fa-file-text-o',
                        'color': 'info',
                        'message': f'{phe_duyet_cho} đề xuất mua chờ phê duyệt',
                    })
            except:
                pass
            
            if notifications:
                html = '<div class="list-group list-group-flush">'
                for notif in notifications:
                    bg_color = '#fff3cd' if notif['color']=='warning' else '#f8d7da' if notif['color']=='danger' else '#d1ecf1'
                    border_color = '#ffc107' if notif['color']=='warning' else '#dc3545' if notif['color']=='danger' else '#17a2b8'
                    html += f'''
                    <div class="list-group-item d-flex align-items-center border-0" 
                         style="background: {bg_color}; border-radius: 10px; margin-bottom: 8px; border-left: 4px solid {border_color} !important;">
                        <i class="fa {notif['icon']} mr-3" style="font-size: 1.2rem;"></i>
                        <span>{notif['message']}</span>
                    </div>
                    '''
                html += '</div>'
                res['thong_bao_html'] = html
            else:
                res['thong_bao_html'] = '''
                <div class="text-center py-4 text-muted">
                    <i class="fa fa-check-circle text-success fa-3x mb-2"></i>
                    <p>Không có thông báo mới</p>
                </div>
                '''
        
        # Tính toán hoạt động gần đây HTML
        if 'hoat_dong_html' in fields_list:
            activities = []
            try:
                DonMuon = self.env['don_muon_tai_san']
                recent_don = DonMuon.search([], limit=5, order='create_date desc')
                for don in recent_don:
                    trang_thai_map = {
                        'nhap': ('Nháp', 'secondary'),
                        'cho_duyet': ('Chờ duyệt', 'warning'),
                        'da_duyet': ('Đã duyệt', 'success'),
                        'tu_choi': ('Từ chối', 'danger'),
                    }
                    status = trang_thai_map.get(don.trang_thai, ('', 'secondary'))
                    activities.append({
                        'icon': 'fa-file-text',
                        'color': status[1],
                        'title': f'Đơn mượn #{don.id}',
                        'desc': f'{don.nhan_vien_muon_id.name or "N/A"} - {status[0]}',
                        'date': don.create_date.strftime('%d/%m/%Y %H:%M') if don.create_date else '',
                    })
            except Exception as e:
                _logger.warning(f"Error getting recent activities: {e}")
            
            if activities:
                html = '<div class="list-group list-group-flush">'
                for act in activities[:5]:
                    html += f'''
                    <div class="list-group-item d-flex align-items-center border-0 px-0">
                        <div style="width: 40px; height: 40px; background: var(--{act['color']}, #6c757d); 
                                    border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                            <i class="fa {act['icon']} text-white"></i>
                        </div>
                        <div class="flex-grow-1">
                            <div class="fw-bold">{act['title']}</div>
                            <small class="text-muted">{act['desc']}</small>
                        </div>
                        <small class="text-muted">{act['date']}</small>
                    </div>
                    '''
                html += '</div>'
                res['hoat_dong_html'] = html
            else:
                res['hoat_dong_html'] = '''
                <div class="text-center py-4 text-muted">
                    <i class="fa fa-inbox fa-3x mb-2"></i>
                    <p>Chưa có hoạt động nào</p>
                </div>
                '''
        
        return res

    @api.depends_context('uid')
    def _compute_currency(self):
        for record in self:
            record.currency_id = self.env.company.currency_id

    @api.depends_context('uid')
    def _compute_stats(self):
        for record in self:
            # Thống kê tài sản
            TaiSan = self.env['tai_san']
            record.total_tai_san = TaiSan.search_count([])
            # Tài sản đang sử dụng = đã phân bổ và chưa thanh lý
            record.active_tai_san = TaiSan.search_count([('trang_thai_thanh_ly', 'in', ['da_phan_bo', 'chua_phan_bo', 'chua_thanh_ly'])])
            
            # Tổng giá trị - FIX: Dùng field đúng
            tai_san_list = TaiSan.search([])
            record.total_value = sum(
                ts.gia_tri_hien_tai or ts.gia_tri_ban_dau or 0 
                for ts in tai_san_list
            )
            
            # Thống kê mượn trả
            try:
                DonMuon = self.env['don_muon_tai_san']
                record.don_cho_duyet = DonMuon.search_count([('trang_thai', '=', 'cho_duyet')])
                record.dang_muon = DonMuon.search_count([('trang_thai', '=', 'da_duyet')])
                
                # Quá hạn - dùng thoi_gian_tra_du_kien thay vì ngay_hen_tra
                MuonTra = self.env['muon_tra_tai_san']
                record.qua_han = MuonTra.search_count([
                    ('trang_thai', '=', 'dang_muon'),
                    ('thoi_gian_tra_du_kien', '<', fields.Datetime.now())
                ])
            except Exception as e:
                _logger.warning(f"Error computing muon_tra stats: {e}")
                record.don_cho_duyet = 0
                record.dang_muon = 0
                record.qua_han = 0


    @api.depends_context('uid')
    def _compute_thong_bao_html(self):
        for record in self:
            notifications = []
            
            # Đơn chờ duyệt
            if record.don_cho_duyet > 0:
                notifications.append({
                    'icon': 'fa-clock-o',
                    'color': 'warning',
                    'message': f'{record.don_cho_duyet} đơn mượn đang chờ duyệt',
                })
            
            # Quá hạn
            if record.qua_han > 0:
                notifications.append({
                    'icon': 'fa-exclamation-triangle',
                    'color': 'danger',
                    'message': f'{record.qua_han} tài sản quá hạn chưa trả',
                })
            
            # Phê duyệt mua
            try:
                PheDuyet = self.env['phe_duyet_mua_tai_san']
                # Dùng field 'state' với giá trị 'draft' thay vì 'trang_thai'/'cho_duyet'
                phe_duyet_cho = PheDuyet.search_count([('state', '=', 'draft')])
                if phe_duyet_cho > 0:
                    notifications.append({
                        'icon': 'fa-file-text-o',
                        'color': 'info',
                        'message': f'{phe_duyet_cho} đề xuất mua chờ phê duyệt',
                    })
            except:
                pass
            
            if notifications:
                html = '<div class="list-group list-group-flush">'
                for notif in notifications:
                    html += f'''
                    <div class="list-group-item d-flex align-items-center border-0" 
                         style="background: {'#fff3cd' if notif['color']=='warning' else '#f8d7da' if notif['color']=='danger' else '#d1ecf1'}; 
                                border-radius: 10px; margin-bottom: 8px; border-left: 4px solid {'#ffc107' if notif['color']=='warning' else '#dc3545' if notif['color']=='danger' else '#17a2b8'} !important;">
                        <i class="fa {notif['icon']} mr-3" style="font-size: 1.2rem;"></i>
                        <span>{notif['message']}</span>
                    </div>
                    '''
                html += '</div>'
                record.thong_bao_html = html
            else:
                record.thong_bao_html = '''
                <div class="text-center py-4 text-muted">
                    <i class="fa fa-check-circle text-success fa-3x mb-2"></i>
                    <p>Không có thông báo mới</p>
                </div>
                '''

    @api.depends_context('uid')
    def _compute_hoat_dong_html(self):
        for record in self:
            activities = []
            
            # Đơn mượn gần đây
            try:
                DonMuon = self.env['don_muon_tai_san']
                recent_don = DonMuon.search([], limit=5, order='create_date desc')
                for don in recent_don:
                    trang_thai_map = {
                        'nhap': ('Nháp', 'secondary'),
                        'cho_duyet': ('Chờ duyệt', 'warning'),
                        'da_duyet': ('Đã duyệt', 'success'),
                        'tu_choi': ('Từ chối', 'danger'),
                    }
                    status = trang_thai_map.get(don.trang_thai, ('', 'secondary'))
                    activities.append({
                        'icon': 'fa-file-text',
                        'color': status[1],
                        'title': f'Đơn mượn #{don.id}',
                        'desc': f'{don.nhan_vien_muon_id.name or "N/A"} - {status[0]}',
                        'date': don.create_date.strftime('%d/%m/%Y %H:%M') if don.create_date else '',
                    })
            except Exception as e:
                _logger.warning(f"Error getting recent activities: {e}")
            
            if activities:
                html = '<div class="list-group list-group-flush">'
                for act in activities[:5]:
                    html += f'''
                    <div class="list-group-item d-flex align-items-center border-0 px-0">
                        <div style="width: 40px; height: 40px; background: var(--{act['color']}, #6c757d); 
                                    border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                            <i class="fa {act['icon']} text-white"></i>
                        </div>
                        <div class="flex-grow-1">
                            <div class="fw-bold">{act['title']}</div>
                            <small class="text-muted">{act['desc']}</small>
                        </div>
                        <small class="text-muted">{act['date']}</small>
                    </div>
                    '''
                html += '</div>'
                record.hoat_dong_html = html
            else:
                record.hoat_dong_html = '''
                <div class="text-center py-4 text-muted">
                    <i class="fa fa-inbox fa-3x mb-2"></i>
                    <p>Chưa có hoạt động nào</p>
                </div>
                '''

    # ============ ACTION BUTTONS ============
    def action_open_don_muon(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Đơn mượn tài sản',
            'res_model': 'don_muon_tai_san',
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def action_open_muon_tra(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Quản lý mượn trả',
            'res_model': 'muon_tra_tai_san',
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def action_open_tai_san(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tài sản',
            'res_model': 'tai_san',
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def action_open_kiem_ke(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Kiểm kê tài sản',
            'res_model': 'kiem_ke_tai_san',
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def action_open_phe_duyet(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Phê duyệt mua tài sản',
            'res_model': 'phe_duyet_mua_tai_san',
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def action_refresh_data(self):
        """Làm mới dữ liệu dashboard - tạo record mới để computed fields tính lại"""
        # Tạo record mới để computed fields tính lại
        new_dashboard = self.create({'name': 'Dashboard'})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Dashboard Tổng quan',
            'res_model': 'dashboard.main',
            'view_mode': 'form',
            'res_id': new_dashboard.id,
            'view_id': self.env.ref('q_trang_chu.view_dashboard_main_form').id,
            'target': 'current',
        }

    # ============ API METHODS ============
    @api.model
    def get_dashboard_data(self):
        """API method trả về dữ liệu dashboard - tích hợp từ cả 2 module"""
        try:
            # ========== TÀI SẢN - từ quan_ly_tai_san ==========
            TaiSan = self.env['tai_san']
            total_tai_san = TaiSan.search_count([])
            # Tài sản đang sử dụng = chưa thanh lý (đã phân bổ, chưa phân bổ, hoặc chưa thanh lý)
            active_tai_san = TaiSan.search_count([('trang_thai_thanh_ly', 'in', ['da_phan_bo', 'chua_phan_bo', 'chua_thanh_ly'])])
            
            # Tổng giá trị - Dùng field đúng
            tai_san_list = TaiSan.search([])
            total_value = sum(
                ts.gia_tri_hien_tai or ts.gia_tri_ban_dau or 0 
                for ts in tai_san_list
            )
            
            # ========== TÀI CHÍNH - từ quan_ly_tai_chinh ==========
            tai_chinh_data = {
                'tong_phe_duyet': 0,
                'phe_duyet_cho_duyet': 0,
                'tong_gia_tri_phe_duyet': 0,
            }
            
            try:
                PheDuyet = self.env['phe_duyet_mua_tai_san']
                tai_chinh_data['tong_phe_duyet'] = PheDuyet.search_count([])
                # Dùng field 'state' với giá trị 'draft' thay vì 'trang_thai'/'cho_duyet'
                tai_chinh_data['phe_duyet_cho_duyet'] = PheDuyet.search_count([('state', '=', 'draft')])
                
                # Tính tổng giá trị phê duyệt
                phe_duyet_list = PheDuyet.search([])
                tai_chinh_data['tong_gia_tri_phe_duyet'] = sum(
                    pd.tong_gia_tri or 0 for pd in phe_duyet_list
                )
            except Exception as e:
                _logger.warning(f"Error fetching financial data: {e}")
            
            # ========== MƯỢN TRẢ TÀI SẢN ==========
            don_cho_duyet = 0
            dang_muon = 0
            qua_han = 0
            
            try:
                DonMuon = self.env['don_muon_tai_san']
                don_cho_duyet = DonMuon.search_count([('trang_thai', '=', 'cho_duyet')])
                dang_muon = DonMuon.search_count([('trang_thai', '=', 'da_duyet')])
                
                # Quá hạn - dùng thoi_gian_tra_du_kien thay vì ngay_hen_tra
                MuonTra = self.env['muon_tra_tai_san']
                qua_han = MuonTra.search_count([
                    ('trang_thai', '=', 'dang_muon'),
                    ('thoi_gian_tra_du_kien', '<', fields.Datetime.now())
                ])
            except Exception as e:
                _logger.warning(f"Error computing muon_tra stats: {e}")
            
            # ========== THÔNG BÁO ==========
            thong_bao = []
            
            # Thông báo từ tài sản
            if don_cho_duyet > 0:
                thong_bao.append({
                    'icon': 'fa-clock-o',
                    'type': 'warning',
                    'message': f'{don_cho_duyet} đơn mượn đang chờ duyệt',
                    'action': 'don_muon_tai_san',
                })
            
            if qua_han > 0:
                thong_bao.append({
                    'icon': 'fa-exclamation-triangle',
                    'type': 'danger',
                    'message': f'{qua_han} tài sản quá hạn chưa trả',
                    'action': 'muon_tra_tai_san',
                })
            
            # Thông báo từ tài chính - dùng 'draft' vì đây là giá trị hiển thị 'Chờ phê duyệt' trong model
            if tai_chinh_data['phe_duyet_cho_duyet'] > 0:
                thong_bao.append({
                    'icon': 'fa-file-text-o',
                    'type': 'info',
                    'message': f'{tai_chinh_data["phe_duyet_cho_duyet"]} đề xuất mua chờ phê duyệt',
                    'action': 'phe_duyet_mua_tai_san',
                })
            
            # ========== HOẠT ĐỘNG GẦN ĐÂY ==========
            hoat_dong_gan_day = []
            try:
                DonMuon = self.env['don_muon_tai_san']
                recent_don = DonMuon.search([], limit=5, order='create_date desc')
                
                trang_thai_map = {
                    'nhap': ('Nháp', 'secondary'),
                    'cho_duyet': ('Chờ duyệt', 'warning'),
                    'da_duyet': ('Đã duyệt', 'success'),
                    'tu_choi': ('Từ chối', 'danger'),
                }
                
                for don in recent_don:
                    status = trang_thai_map.get(don.trang_thai, ('', 'secondary'))
                    hoat_dong_gan_day.append({
                        'icon': 'fa-file-text',
                        'color': status[1],
                        'title': f'Đơn mượn #{don.id}',
                        'description': f'{don.nhan_vien_muon_id.name or "N/A"} - {status[0]}',
                        'date': don.create_date.strftime('%d/%m/%Y %H:%M') if don.create_date else '',
                    })
            except Exception as e:
                _logger.warning(f"Error getting recent activities: {e}")
            
            return {
                'tai_san': {
                    'total': total_tai_san,
                    'active': active_tai_san,
                    'dang_muon': dang_muon,
                    'total_value': total_value,
                    'depreciated_value': 0,
                },
                'tai_chinh': tai_chinh_data,
                'muon_tra': {
                    'don_cho_duyet': don_cho_duyet,
                    'don_dang_muon': dang_muon,
                    'qua_han': qua_han,
                },
                'thong_bao': thong_bao,
                'hoat_dong_gan_day': hoat_dong_gan_day,
            }
        except Exception as e:
            _logger.error(f"Error in get_dashboard_data: {e}")
            return {
                'tai_san': {'total': 0, 'active': 0, 'dang_muon': 0, 'total_value': 0, 'depreciated_value': 0},
                'tai_chinh': {'tong_phe_duyet': 0, 'phe_duyet_cho_duyet': 0, 'tong_gia_tri_phe_duyet': 0},
                'muon_tra': {'don_cho_duyet': 0, 'don_dang_muon': 0, 'qua_han': 0},
                'thong_bao': [],
                'hoat_dong_gan_day': [],
            }

    @api.model
    def get_chart_data(self, chart_type):
        """API method trả về dữ liệu biểu đồ"""
        if chart_type == 'tai_san_theo_danh_muc':
            return self._get_assets_by_category()
        elif chart_type == 'muon_tra_theo_thang':
            return self._get_borrowing_by_month()
        return {}

    def _get_assets_by_category(self):
        """Tài sản theo danh mục"""
        result = []
        try:
            DanhMuc = self.env['danh_muc_tai_san']
            TaiSan = self.env['tai_san']
            
            for dm in DanhMuc.search([]):
                count = TaiSan.search_count([('danh_muc_id', '=', dm.id)])
                if count > 0:
                    result.append({
                        'name': dm.ten_danh_muc,
                        'value': count,
                    })
        except:
            pass
        return result

    def _get_borrowing_by_month(self):
        """Số lượt mượn theo tháng"""
        result = []
        try:
            DonMuon = self.env['don_muon_tai_san']
            for i in range(5, -1, -1):
                month_start = datetime.now().replace(day=1) - timedelta(days=i*30)
                month_end = month_start + timedelta(days=30)
                count = DonMuon.search_count([
                    ('create_date', '>=', month_start),
                    ('create_date', '<', month_end),
                ])
                result.append({
                    'month': month_start.strftime('%m/%Y'),
                    'count': count,
                })
        except:
            pass
        return result
