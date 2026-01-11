{
    'name': 'Farm Mobile Workbench',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Mobile-first UI for Field Operations and Scanning',
    'description': """
        Mobile module for Odoo 19 Farm Management System.
        - Field Operator Workbench (Large buttons, simplified tasks) [US-10]
        - QR/Barcode Quick Actions (Scan to Feeding, Scan to Harvest) [US-11]
        - Optimized Mobile Dashboards (PWA ready)
    """,
    'author': 'Jeffery',
    'depends': ['farm_operation', 'farm_livestock', 'farm_iot', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/farm_mobile_menus.xml',
        'views/farm_mobile_dashboard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'farm_mobile/static/src/scss/farm_mobile.scss',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}