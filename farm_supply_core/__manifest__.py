{
    'name': 'Farm Supply Chain Core',
    'version': '19.0.1.0.0',
    'category': 'Industries/Agriculture',
    'summary': 'Core Supply Chain Infrastructure and Base Models',
    'description': """
        Core Supply Chain module for Odoo 19 Farm Management System.
        - Base supply chain models and infrastructure
        - Supply chain node definitions
        - Common supply chain utilities and mixins
    """,
    'author': 'genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>',
    'website': 'http://www.geninit.cn',
    'depends': [
        'base',
        'mail',
        'farm_core',
    ],
    'data': [
        'views/menu.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}