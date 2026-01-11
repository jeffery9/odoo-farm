{
    'name': 'Farm Marketing & Traceability',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Consumer Traceability, Marketing QR Codes and Brand Story',
    'description': """
        Marketing module for Odoo 19 Farm Management System.
        - Consumer-facing Traceability Portal [US-15]
        - Product Story & Quality Certificate Display
        - Integration with Agritourism & CRM
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'farm_quality', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/traceability_templates.xml',
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
