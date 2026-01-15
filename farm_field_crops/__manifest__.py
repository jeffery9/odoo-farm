{
    'name': 'Farm Field Crops',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Field Crops Management - Plots, Sowing, Harvesting, Mechanized Operations',
    'description': """
        Field Crops Management Module for Odoo 19 Farm Management System.

        Features:
        - Field crop plot management with specific field crops attributes
        - Sowing and harvesting operations for field crops
        - Mechanized operations tracking for large scale farming
        - Planting density and seeding rate management
        - Fertilizer application planning and tracking
        - Large scale irrigation management
        - Harvest yield tracking and analysis
    """,
    'author': 'Jeffery',
    'depends': [
        'farm_core',
        'farm_operation',
        'farm_mrp',
        'project',
        'stock',
        'mrp',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/field_crop_operation_views.xml',
        'views/crop_isl_views.xml',
        'views/menu.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}