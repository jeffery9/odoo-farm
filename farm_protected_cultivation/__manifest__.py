{
    'name': 'Farm Protected Cultivation',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Protected Cultivation Management - Greenhouse, Environment Control, Water-Fertilizer Integration',
    'description': """
        Protected Cultivation Management Module for Odoo 19 Farm Management System.

        Features:
        - Greenhouse/protected structure management
        - Environmental control system integration (temperature, humidity, CO2, lighting)
        - Water-fertilizer integration system management
        - Climate monitoring and control
        - Automated irrigation and fertigation
        - Protected cultivation specific crop management
        - Environmental data logging and analysis
    """,
    'author': 'Jeffery',
    'depends': [
        'farm_core',
        'farm_operation',
        'farm_iot',
        'project',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/protected_cultivation_operation_views.xml',
        'views/menu.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}