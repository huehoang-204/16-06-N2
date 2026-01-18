# -*- coding: utf-8 -*-
{
    'name': "quan_ly_tai_chinh",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Quản lý tài chính
    """,

    'author': "Hoàng Phương Huế - Nguyễn Lê Việt Hoàng - Nguyễn Trung Thành -1606",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'quan_ly_tai_san', 'nhan_su', 'account', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/tai_chinh_demo.xml',  # ← THÊM vào đây để luôn load
        'views/khau_hao_tai_san_views.xml',
        'views/but_toan_views.xml',
        'views/tai_khoan_quan_tri_views.xml',
        'views/bao_cao_tai_chinh_views.xml',
        'views/phe_duyet_mua_tai_san_views.xml',
        'views/dashboard_tai_chinh_views.xml',
        'views/tinh_toan_khau_hao_views.xml',
        'views/wizard_sao_chep_views.xml',
        'report/bao_cao_tai_chinh_report.xml',
        'views/menu.xml',  # PHẢI LOAD CUỐI CÙNG sau khi tất cả actions đã được định nghĩa
    ],
    'assets': {
        'web.assets_backend': [
            'quan_ly_tai_chinh/static/css/bao_cao_style.css',
            'quan_ly_tai_chinh/static/js/bao_cao_charts.js',
        ],
    },
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
