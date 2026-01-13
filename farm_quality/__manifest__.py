{
    'name': 'Farm Quality Control',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Quality Control Points, Checks and Traceability',
    'description': """
        Quality module for Odoo 19 Farm Management System.
        - Quality Control Points (QCP) definition [US-01-04]
        - Quality Checks (Pass/Fail, Measurements) [US-15-02]
        - Quality Alerts & Traceability [US-02-01]
    """,
    'author': 'Jeffery',
    'depends': ['farm_operation', 'farm_core'],
    'data': [
        'security/ir.model.access.csv',
        'data/quality_data.xml',
        'views/quality_point_views.xml',
        'views/quality_check_views.xml',
        'views/quality_alert_views.xml',
        'views/stock_lot_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
