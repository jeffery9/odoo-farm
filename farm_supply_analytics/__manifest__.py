{
    'name': 'Farm Supply Analytics',
    'version': '19.0.1.0.0',
    'category': 'Industries/Agriculture',
    'summary': 'Supply Chain Analytics and Visualization',
    'description': """
        Supply Analytics module for Odoo 19 Farm Management System.
        - Supply Chain Visualization (Control Tower) [US-084-01]
        - Demand Forecasting & Inventory Optimization [US-084-02]
        - Supply Chain Risk Management [US-084-03]
        - Real-time KPIs and monitoring
    """,
    'author': 'genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>',
    'website': 'http://www.geninit.cn',
    'depends': [
        'base',
        'mail',
        'farm_core',
        'farm_supply_core',
        'farm_ai_decision',
    ],
    'data': [
        'views/menu.xml',
        'security/ir.model.access.csv',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}