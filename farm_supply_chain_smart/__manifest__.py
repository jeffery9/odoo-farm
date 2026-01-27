{
    'name': 'Farm Smart Supply Chain',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'AI-driven Supply Chain Visualization and Optimization',
    'description': """
        Smart Supply Chain module for Odoo 19.
        - Supply Chain Visualization (Control Tower) [US-54-01]
        - Demand Forecasting & Inventory Optimization [US-54-02]
        - Supply Chain Risk Management [US-54-03]
    """,
    'author': 'genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>',
    'website': 'http://www.geninit.cn',
    'depends': ['farm_core', 'farm_supply', 'farm_logistics', 'farm_ai_decision'],
    'data': [
        'security/ir.model.access.csv',
        'views/smart_supply_chain_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}