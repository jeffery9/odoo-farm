{
    'name': 'Farm Apiculture',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Apiculture Management - Bee Colonies, Hive Management, Honey Production, Nectar Source Tracking',
    'description': """
        Apiculture Management Module for Odoo 19 Farm Management System.

        Features:
        - Bee colony management
        - Hive positioning and tracking
        - Nectar source tracking and management
        - Bee migration tracking
        - Honey production and quality management
        - Bee health and disease management
        - Seasonal beekeeping operations
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
        'views/menu.xml',
        'views/apiculture_operation_views.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}