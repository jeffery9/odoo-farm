{
    'name': 'Farm Orchard Horticulture',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Orchard Horticulture Management - Fruit Trees, Pruning, Lifecycle, Harvest Tracking',
    'description': """
        Orchard Horticulture Management Module for Odoo 19 Farm Management System.

        Features:
        - Fruit tree individual plant management
        - Pruning records and schedule management
        - Flowering period management
        - Harvest tracking for tree-based crops
        - Annual growth cycle tracking
        - Orchard specific crop management
        - Tree lifecycle and age-based management
    """,
    'author': 'Jeffery',
    'depends': [
        'farm_core',
        'farm_operation',
        'project',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/orchard_operation_views.xml',
        'views/menu.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}