{
    'name': 'Farm Supply Chain',
    'version': '19.0.1.0.0',
    'category': 'Industries/Agriculture',
    'summary': 'Core Supply Chain Infrastructure',
    'description': """
        Supply Chain foundation module for Odoo 19 Farm Management System.
        (Consolidated from farm_supply and farm_supply)
        
        - Base supply chain models and infrastructure
        - Supply chain node definitions
        - Common supply chain utilities and mixins
    """,
    'author': 'Jeffery',
    'depends': [
        'base',
        'mail',
        'farm_core',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}
