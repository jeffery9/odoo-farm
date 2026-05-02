{
    'name': 'Farm Supply Quality & Pricing',
    'version': '19.0.1.0.0',
    'category': 'Industries/Agriculture',
    'summary': 'Quality-based Pricing for Agricultural Procurement',
    'description': """
        Supply Quality module for Odoo 19 Farm Management System.
        - Quality-based Procurement Pricing [US-09-11]
        - Acquisition Pricing with Multiple Quality Metrics [US-09-19]
        - Quality grading and adjustment algorithms
    """,
    'author': 'genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>',
    'website': 'http://www.geninit.cn',
    'depends': [
        'base',
        'mail',
        'farm_core',
        'farm_supply_core',
        'farm_supply_procurement',
        'purchase',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}