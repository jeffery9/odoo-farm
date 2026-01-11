{
    'name': 'Farm Supply & Inputs',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Agricultural Input Management, Procurement and Compliance',
    'description': """
        Supply module for Odoo 19 Farm Management System.
        - Agricultural Input Catalog (Seeds, Fertilizers, Pesticides, Feed)
        - Purchase Order Integration with Safety Checks
        - Input Usage Forecasting and Stock Alerts
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'purchase', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/farm_input_views.xml',
        'views/purchase_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
