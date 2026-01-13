{
    'name': 'Farm Land Management (China)',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'China-specific Land Contract Rights and Land Use Control',
    'description': """
        Implements China's land management regulations [US-18-01].
        - Land Contract Rights Certificate Tracking
        - Land Use Control Validation (e.g., Permanent Basic Farmland protection)
        - Prevents illegal land use for specific agricultural activities.
    """,
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "website": "http://www.geninit.cn",
    'depends': ['farm_core', 'farm_operation'],
    'data': [
        'security/ir.model.access.csv',
        'views/land_mgmt_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
