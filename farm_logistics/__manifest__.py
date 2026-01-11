{
    'name': 'Farm Logistics',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Cold Chain, Packaging and Farm Direct Logistics',
    'description': """
        Logistics module for Odoo 19 Farm Management System.
        - Cold Chain Management (Temperature tracking) [US-30]
        - Multi-level Packaging support
        - Integrated Field Delivery
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/logistics_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
