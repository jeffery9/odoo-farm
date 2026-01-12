{
    'name': 'Farm Subsidy Management',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Government Subsidies and Policy Compliance',
    'description': """
        Manage agricultural subsidies and policy compliance [US-17-02].
        - Subsidy Programs (e.g. Organic Conversion, Crop Rotation)
        - Application Tracking & Reporting
        - Linking Subsidies to Land Parcels
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/subsidy_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
