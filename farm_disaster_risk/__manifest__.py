{
    'name': 'Farm Disaster Risk Management',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Meteorological Disaster Warning and Loss Assessment Integration',
    'description': """
        Integrates meteorological disaster warnings and manages loss assessment processes [US-17-10].
        - Automatically creates disaster incidents based on weather alerts.
        - Records details of disaster events (hail, frost, flood).
        - Links to affected land parcels and triggers draft loss assessments.
        - Supports integration with insurance claims processes.
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'farm_weather', 'farm_crisis', 'farm_operation'],
    'data': [
        'security/ir.model.access.csv',
        'views/disaster_risk_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
