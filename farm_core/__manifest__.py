{
    'name': 'Farm Core',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Core Agricultural Master Data and Activity Classification',
    'description': """
        Base module for Odoo 19 Farm Management System.
        - Agricultural Activity Classification (US-01)
        - Sector-specific attributes (US-02)
        - Land Parcel Management (US-03)
        - Biological Asset Management (US-04)
    """,
    'author': 'Jeffery',
    'depends': ['project', 'stock'],
    'data': [
        'security/farm_security.xml',
        'security/ir.model.access.csv',
        'views/farm_activity_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
