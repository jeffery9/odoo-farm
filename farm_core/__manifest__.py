{
    'name': 'Farm Core',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Core Agricultural Master Data and Industry Configuration',
    'icon': '/farm_core/static/description/icon.svg',
    'description': """
        Base module for Odoo 19 Farm Management System.
        - Agricultural Activity Classification (US-01-01)
        - Sector-specific attributes (US-01-02)
        - Land Parcel Management (US-01-03)
        - Biological Asset Management (US-01-04)
        - Industry Configuration Management
        - Biological Asset Valuation and Depreciation (US-01-07)
        - One-Click Industry Data Package Initialization (US-01-08)
    """,
    'author': 'Jeffery',
    'depends': ['project', 'stock', 'uom', 'base_setup'],
    'data': [
        'security/farm_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/product_category_data.xml',
        'data/ir_cron_data.xml',
        'views/biological_asset_management_views.xml',
        'views/land_location_management_views.xml',
        'views/activity_operation_management_views.xml',
        'views/geofencing_management_views.xml',
        'views/config_setup_management_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'data/farm_demo_data.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
    'post_init_hook': 'post_init_hook',
}
