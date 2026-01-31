{
    'name': 'Farm Circular Economy',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Circular Economy and Resource Flow Models',
    'description': """
        Circular economy module for Odoo 19 Farm Management System.
        - Circular flow economics
        - Resource utilization optimization
        - Waste-to-resource conversion tracking
    """,
    'author': 'Jeffery',
    'depends': [
        'base',
        'mail',
        'farm_core',
        'farm_operation',
        'farm_esg',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/circular_flow_views.xml',
        'data/ir_sequence_data.xml',
        'data/sustainability_data.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}