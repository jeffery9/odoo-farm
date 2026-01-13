{
    'name': 'Farm Entity Registration (China)',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'China-specific Management of Family Farm / Cooperative Registration Info',
    'description': """
        Maintains registration information for family farms and agricultural cooperatives [US-18-08].
        - Tracks unified social credit code, registration number, and member lists.
        - Stores electronic certificates with expiry date reminders.
        - Ensures compliance with Chinese agricultural entity regulations.
    """,
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "website": "http://www.geninit.cn",
    'depends': ['base', 'farm_core'],
    'data': [
        'security/ir.model.access.csv',
        'views/entity_reg_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
