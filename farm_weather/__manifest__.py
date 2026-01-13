{
    'name': 'Farm Weather Forecast',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Weather Forecast Integration for Farm Management',
    'description': """
        Weather module for Odoo 19 Farm Management System.
        - Fetch 7-day weather forecast via external API
        - Link weather to GIS locations (parcels)
        - Weather-based alerts (Frost, Storm, High Temp)
    """,
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "website": "http://www.geninit.cn",
    'depends': ['farm_core', 'farm_iot'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/weather_forecast_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
