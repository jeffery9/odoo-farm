{
    'name': 'Farm Supply Logistics',
    'version': '19.0.1.0.0',
    'category': 'Industries/Agriculture',
    'summary': 'Cold Chain, Packaging and Farm Direct Logistics',
    'description': """
        Logistics module for Odoo 19 Farm Management System.
        - Cold Chain Management (Temperature tracking) [US-003-03]
        - Multi-level Packaging support
        - Integrated Field Delivery
        - Cold Storage Multi-zone and Humidity Management [US-009-09]
        - Post-harvest Pre-cooling Process Tracking [US-009-08]
        - Dynamic Shelf-life Prediction based on IoT Temperature [US-009-07]
    """,
    'author': 'genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>',
    'website': 'http://www.geninit.cn',
    'depends': [
        'base',
        'mail',
        'farm_core',
        'farm_supply',
        'stock',
    ],
    'data': [
        'views/menu.xml',
        #'security/ir.model.access.csv',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}