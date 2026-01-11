{
    'name': 'Farm Livestock',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Livestock and Aquaculture management, Feeding and Groups',
    'description': """
        Livestock module for Odoo 19 Farm Management System.
        - Feeding Plans & Formulas (BOM based) [US-09]
        - Biological Asset Tracking [US-04 integration]
        - Group Movements (Merge, Split, Death) [US-12]
    """,
    'author': 'Jeffery',
    'depends': ['farm_operation', 'farm_core'],
    'data': [
        'security/ir.model.access.csv',
        'views/livestock_feeding_views.xml',
    ],
    'demo': [
        'data/farm_livestock_demo.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}