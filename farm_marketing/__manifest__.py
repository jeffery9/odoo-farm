{
    'name': 'Farm Marketing & Traceability',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Consumer Traceability, Marketing QR Codes and Brand Story',
    'description': """
        Marketing module for Odoo 19 Farm Management System.
        - Consumer-facing Traceability Portal [US-08-01]
        - Product Story & Quality Certificate Display
        - Integration with Agritourism & CRM
        - Expiry Warning and Promotional Linkage [US-14-14]
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'farm_quality', 'farm_operation', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/farm_lot_views.xml',
        'views/traceability_templates.xml',
        'views/product_template_views.xml',
        'views/partner_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
