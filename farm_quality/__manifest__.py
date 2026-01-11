{
    'name': 'Farm Quality Control',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Quality Control Points, Checks and Traceability',
    'description': """
        Quality module for Odoo 19 Farm Management System.
        - Quality Control Points (QCP) definition [US-13]
        - Quality Checks (Pass/Fail, Measurements) [US-14]
        - Quality Alerts & Traceability [US-15]
    """,
    'author': 'Jeffery',
    'depends': ['farm_operation', 'farm_core'],
    'data': [
        'security/ir.model.access.csv',
        'views/quality_point_views.xml',
        'views/quality_check_views.xml',
        'views/quality_alert_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
