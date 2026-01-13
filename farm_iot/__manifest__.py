{
    'name': 'Farm IOT',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'IIOT Telemetry Data and Device Management',
    'description': """
        IOT module for Odoo 19 Farm Management System.
        - Telemetry Data Collection (Temperature, PH, DO, etc.) [US-11-03, US-02-02]
        - Threshold Alerts [US-06-02]
        - Storage Environment Monitoring and Alerts [US-14-06]
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'project', 'industrial_iot'],
    'data': [
        'security/ir.model.access.csv',
        'views/farm_telemetry_views.xml',
        'views/farm_automation_views.xml',
        'views/storage_env_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
