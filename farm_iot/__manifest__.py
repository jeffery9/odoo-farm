{
    'name': 'Farm IOT',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'IIOT Telemetry Data and Device Management',
    'description': """
        IOT module for Odoo 19 Farm Management System.
        - Telemetry Data Collection (Temperature, PH, DO, etc.) [US-11, US-19]
        - Threshold Alerts [US-20]
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'project', 'industrial_iot'],
    'data': [
        'security/ir.model.access.csv',
        'views/farm_telemetry_views.xml',
        'views/farm_automation_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
