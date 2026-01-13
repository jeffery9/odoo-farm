{
    'name': 'Farm Dashboard & Cockpit',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Unified Management Dashboard for Odoo Farm',
    'icon': '/farm_dashboard/static/description/icon.svg',
    'description': """
        Dashboard module for Odoo 19 Farm Management System.
        - Integrated view of production, inventory and weather
        - Resource availability overview
        - Critical alerts and safety status
    """,
    'author': 'Jeffery',
    'depends': ['farm_operation', 'farm_weather', 'farm_iot', 'farm_financial'],
    'data': [
        'views/farm_dashboard_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}
