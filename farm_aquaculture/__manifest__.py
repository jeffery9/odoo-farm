{
    'name': 'Farm Aquaculture',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Aquaculture Management - Water Quality, Feeding, Growth Tracking, Dissolved Oxygen Monitoring',
    'description': """
        Aquaculture Management Module for Odoo 19 Farm Management System.

        Features:
        - Water quality monitoring and management
        - Aquatic species feeding management
        - Growth tracking for aquatic species
        - Dissolved oxygen and pH monitoring
        - Pond/tank management
        - Aquaculture specific harvest management
        - Water treatment and circulation management
    """,
    'author': 'Jeffery',
    'depends': [
        'farm_core',
        'farm_operation',
        'farm_mrp',
        'farm_iot',
        'project',
        'stock',
        'mrp',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/aquaculture_operation_views.xml',
        'views/aquaculture_isl_views.xml',
        'views/menu.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}