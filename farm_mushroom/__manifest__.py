{
    'name': 'Farm Mushroom Cultivation',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Mushroom Cultivation Management - Multi-Batch, Environmental Control, Harvest Records, Multi-Harvest Tracking',
    'description': """
        Mushroom Cultivation Management Module for Odoo 19 Farm Management System.

        Features:
        - Multi-batch cultivation management
        - Environmental control for mushroom growth
        - Harvest records for multiple harvests from same substrate
        - Mushroom strain and spawn management
        - Flush/successive harvest tracking
        - Substrate preparation and management
        - Mushroom specific growth cycle management
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
        'views/mushroom_operation_views.xml',
        'views/menu.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}