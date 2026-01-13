{
    'name': 'Farm Machinery & Equipment',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Agricultural Machinery Management, Fuel Logs and Usage Tracking',
    'description': """
        Equipment module for Odoo 19 Farm Management System.
        - Extension of Maintenance module for Agriculture [US-05-03]
        - Machinery details (Horsepower, Fuel Type, Linkage)
        - Usage & Fuel Logging linked to Operations
    """,
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "website": "http://www.geninit.cn",
    'depends': ['farm_operation', 'maintenance'],
    'data': [
        'security/ir.model.access.csv',
        'views/farm_equipment_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
