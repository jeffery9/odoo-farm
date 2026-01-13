{
    'name': 'Farm Certification & Compliance',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Organic, Green and GI Certification Management',
    'description': """
        Certification module for Odoo 19 Farm Management System.
        - Manage Certification Levels (Organic, Green, Conventional)
        - Track Organic Conversion Periods
        - Certificate Document Management & Expiry Alerts
        - Automatic Certification Inheritance for Harvested Lots
    """,
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "website": "http://www.geninit.cn",
    'depends': ['farm_core', 'farm_operation'],
    'data': [
        'security/ir.model.access.csv',
        'views/certification_views.xml',
        'views/certification_report.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
