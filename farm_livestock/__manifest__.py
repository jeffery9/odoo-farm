{
    'name': 'Farm Livestock',
    'version': '1.1',
    'category': 'Industries/Agriculture',
    'summary': 'Livestock Management - Breeding Records, Health Records, Breeding Management, Individual Identification',
    'description': """
        Livestock Management Module for Odoo 19 Farm Management System.

        Features:
        - Individual animal identification and tracking
        - Breeding records and pedigree management
        - Health records and veterinary tracking
        - Feeding Plans & Formulas (BOM based) [US-01-03]
        - Biological Asset Tracking [US-01-04 integration]
        - Group Movements (Merge, Split, Death) [US-05-04]
        - Breeding management and reproduction tracking
        - Animal lifecycle and age-based management
    """,
    'author': 'Jeffery',
    'depends': ['farm_operation', 'farm_core', 'project', 'mrp', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/livestock_lot_views.xml',
        'views/livestock_advanced_views.xml',
        'views/livestock_feeding_views.xml',
        'views/livestock_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'data/farm_livestock_demo.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}