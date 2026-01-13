{
    'name': 'Farm Data Exchange (DAPLOS/TELEPAC)',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Support for DAPLOS, TELEPAC and Agri-EDI formats',
    'description': """
        Data exchange module for Odoo 19 Farm Management System.
        - Export/Import agricultural data in DAPLOS format
        - Support for TELEPAC (EU CAP) compliance data
        - Generic Agri-EDI interface
    """,
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "website": "http://www.geninit.cn",
    'depends': ['farm_operation'],
    'data': [
        'security/ir.model.access.csv',
        'views/exchange_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
