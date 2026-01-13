{
    'name': 'Farm Livestock',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Livestock and Aquaculture management, Feeding and Groups',
    'description': """
        Livestock module for Odoo 19 Farm Management System.
        - Feeding Plans & Formulas (BOM based) [US-01-03]
        - Biological Asset Tracking [US-01-04 integration]
        - Group Movements (Merge, Split, Death) [US-05-04]
    """,
    'author': 'Jeffery',
    'depends': ['farm_operation', 'farm_core'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/livestock_lot_views.xml',
        'views/livestock_feeding_views.xml',
    ],
    'demo': [
        'data/farm_livestock_demo.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}