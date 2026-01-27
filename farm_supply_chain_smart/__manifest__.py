{
    'name': 'Farm Smart Supply Chain (DEPRECATED)',
    'version': '19.0.1.0.0',
    'category': 'Industries/Agriculture',
    'summary': 'DEPRECATED - Use farm_supply_analytics module instead',
    'description': """
        DEPRECATED: Smart Supply Chain module for Odoo 19.

        This module has been deprecated. Supply chain visualization and analytics
        functionality is now available in the farm_supply_analytics module.

        Please use farm_supply_analytics for supply chain control tower,
        demand forecasting, and risk management.
    """,
    'author': 'genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>',
    'website': 'http://www.geninit.cn',
    'depends': [
        'farm_core',
        'farm_supply_core',
        'farm_supply_analytics',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}