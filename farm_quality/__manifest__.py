{
    'name': 'Farm Quality Control',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Quality Control Points, Checks and Traceability',
    'description': """
        Quality module for Odoo 19 Farm Management System.
        - Quality Control Points (QCP) definition [US-038-04]
        - Quality Checks (Pass/Fail, Measurements) [US-038-02]
        - Quality Alerts & Traceability [US-002-01]
    """,
    'author': 'Jeffery',
    'depends': ['farm_operation', 'farm_core'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        # 'data/quality_data.xml',
        'views/quality_point_views.xml',
        'views/quality_check_views.xml',
        'views/quality_alert_views.xml',
        'views/quality_record_book_views.xml',
        'views/stock_lot_views.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'assets': {
        'web.assets_backend': [
            'farm_quality/static/src/components/**/*.js',
            'farm_quality/static/src/components/**/*.xml',
            'farm_quality/static/src/components/**/*.scss',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
