{
    'name': 'Farm Certificate (China)',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'China-specific Agricultural Product Compliance Certificate',
    'description': """
        Automatically generates "Commitment to Compliance Certificates" for edible agricultural products [US-67].
        - Includes producer, origin, lot, test results, and commitment statement.
        - Integrates QR code for traceability and auto-generation on dispatch.
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'stock', 'farm_marketing'],
    'data': [
        'security/ir.model.access.csv',
        'report/certificate_report_templates.xml',
        'report/certificate_reports.xml',
        'views/certificate_views.xml',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
