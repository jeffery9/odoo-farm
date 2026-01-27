{
    'name': 'Farm Supply Logistics',
    'version': '19.0.1.0.0',
    'category': 'Industries/Agriculture',
    'summary': 'Cold Chain, Packaging and Farm Direct Logistics',
    'description': """
        Logistics module for Odoo 19 Farm Management System.
        - Cold Chain Management (Temperature tracking) [US-03-03]
        - Multi-level Packaging support
        - Integrated Field Delivery
        - Cold Storage Multi-zone and Humidity Management [US-09-09]
        - Post-harvest Pre-cooling Process Tracking [US-09-08]
        - Dynamic Shelf-life Prediction based on IoT Temperature [US-09-07]
    """,
    'author': 'genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>',
    'website': 'http://www.geninit.cn',
    'depends': [
        'base',
        'mail',
        'farm_core',
        'farm_supply_core',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/logistics_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}