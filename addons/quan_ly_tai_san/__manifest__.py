# -*- coding: utf-8 -*-
{
    'name': "quan_ly_tai_san",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Quản lý tài sản của Doanh Nghiệp
    """,

    'author': "Hoàng Phương Huế",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listinga
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'nhan_su', 'hr', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/tai_san_demo.xml',  # ← THÊM vào đây để luôn load
        'views/danh_muc_tai_san.xml',
        'views/kiem_ke_tai_san.xml',
        'views/lich_su_khau_hao.xml',
        'views/luan_chuyen_tai_san.xml',
        'views/don_muon_tai_san.xml',
        'views/muon_tra_tai_san.xml',
        'views/phan_bo_tai_san.xml',
        'views/tai_san.xml',
        'views/thanh_ly_tai_san.xml',
        'views/de_xuat_mua_tai_san_views.xml',
        'views/lich_su_ky_thuat_views.xml',
        'views/dashboard_overview.xml',
        'views/dashboard_borrowing.xml',
        'views/menu.xml',
        'wizard/muon_tra_wizard_views.xml',
        
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
    
    'assets': {
        'web.assets_common': [  # THAY ĐỔI: Dùng assets_common thay vì backend
            'quan_ly_tai_san/static/src/js/moment_locale_fix.js',
        ],
        'web.assets_backend': [
            'quan_ly_tai_san/static/src/js/date_picker_fix.js',
            'https://cdn.jsdelivr.net/npm/chart.js@3.7.1/dist/chart.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.4/moment-with-locales.min.js',
            'quan_ly_tai_san/static/src/css/dashboard.css',
            'quan_ly_tai_san/static/src/js/dashboard_overview.js',
            'quan_ly_tai_san/static/src/js/dashboard_borrowing.js',
        ],
    },
    
    'installable': True,
    'application': True,
}