{
    'name': 'Farm Logistics',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Cold Chain, Packaging and Farm Direct Logistics',
    'description': """
        Logistics module for Odoo 19 Farm Management System.
        - Cold Chain Management (Temperature tracking) [US-03-03, US-14-11]
        - Multi-level Packaging support
        - Integrated Field Delivery
        - Temperature Curve Tracking for Logistics [US-14-11]
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
