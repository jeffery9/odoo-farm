{
    'name': 'Farm Medicinal Plants',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Medicinal Plants Management - GMP Compliance, Active Ingredient Tracking, Certification',
    'description': """
        Medicinal Plants Management Module for Odoo 19 Farm Management System.

        Features:
        - GMP (Good Manufacturing Practice) compliance management
        - Active ingredient tracking and analysis
        - Medicinal plant certification management
        - Harvest timing based on active ingredient levels
        - Quality control for medicinal compounds
        - Compliance with pharmaceutical standards
        - Batch tracking for medicinal plant products
    """,
    'author': 'Jeffery',
    'depends': [
        'farm_core',
        'farm_operation',
        'farm_quality',
        'project',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/medicinal_plants_operation_views.xml',
        'views/menu.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}