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
    """,
    'author': 'Jeffery',
    'depends': ['project', 'stock', 'uom', 'base_setup'],
    'data': [
        'security/farm_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/product_category_data.xml',
        'data/ir_cron_data.xml',
        'views/farm_activity_views.xml',
        'views/farm_location_views.xml',
        'views/product_template_views.xml',
        'views/soil_analysis_views.xml',
        'views/farm_geofence_views.xml',
        'views/res_config_settings_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'data/farm_demo_data.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
