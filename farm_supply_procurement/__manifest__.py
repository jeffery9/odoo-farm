{
    'name': 'Farm Supply Procurement',
    'version': '19.0.1.0.0',
    'category': 'Industries/Agriculture',
    'summary': 'Agricultural Input Management and Procurement',
    'description': """
        Supply Procurement module for Odoo 19 Farm Management System.
        - Agricultural Input Catalog (Seeds, Fertilizers, Pesticides, Feed)
        - Purchase Order Integration with Safety Checks
        - Input Usage Forecasting and Stock Alerts
        - Joint Procurement for Cooperatives [US-09-15]
        - VMI (Vendor Managed Inventory) Automation [US-09-14]
    """,
    'author': 'genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>',
    'website': 'http://www.geninit.cn',
    'depends': [
        'base',
        'mail',
        'farm_core',
        'farm_supply_core',
        'purchase',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/procurement_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}