{
    'name': 'Farm Sustainability & Environment',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Sustainability Indicators, Fertilizer Reduction and Ecological Buffers',
    'description': """
        Sustainability module for Odoo 19 Farm Management System.
        - Monitoring Fertilizer (N/P/K) Reduction Trends [US-08-03]
        - Ecological Buffer Zone Maintenance Records
        - Environmental Impact Dashboards
    """,
    'author': 'Jeffery',
    'depends': ['farm_operation', 'farm_core'],
    'data': [
        'security/ir.model.access.csv',
        'views/sustainability_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
