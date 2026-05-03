{
    'name': 'Farm Carbon Extensions',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Product Carbon Factors, MRP Carbon Calculations, and Batch Carbon Tracking',
    'description': """
        Carbon extension module for Odoo 19 Farm Management System.
        - Product carbon emission factors
        - MRP production carbon calculation
        - Stock lot carbon footprint tracking
    """,
    'author': 'Jeffery',
    'depends': [
        'base',
        'mail',
        'product',
        'mrp',
        'stock',
        'farm_core',
        'farm_operation',
        'farm_esg',
    ],
    'data': [
        # No specific model access rights needed since this module only extends existing models
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}