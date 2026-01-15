{
    'name': 'Farm Agricultural Processing (Industry Profile)',
    'version': '1.1',
    'category': 'Industries/Agriculture',
    'summary': 'Industry-specific configurations and views for agricultural processing',
    'description': """
        This module provides the industry-specific layer for Agricultural Processing.
        It depends on the core logic provided by 'farm_processing'.

        Features:
        - Industry-specific configuration (Industry Settings)
        - Pre-configured menus for Baking, Winemaking, etc.
        - Simplified views tailored for agri-processing workers.
        - Industry dashboards for Yield and Loss analysis.
    """,
    'author': 'Jeffery',
    'depends': [
        'farm_processing',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sc_license_views.xml',
        'views/mrp_processing_industry_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}