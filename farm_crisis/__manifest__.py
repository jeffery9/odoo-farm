{
    'name': 'Farm Crisis & Emergency Response',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Emergency Protocols and Crisis Management SOPs',
    'description': """
        Manage agricultural emergencies and crisis response [US-040-03].
        - Emergency Protocols (SOPs for Disease, Fire, Contamination)
        - Crisis Mode Activation & Asset Lockdown
        - Incident Logging & Reporting
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'farm_safety', 'sale'],
    'data': [
        #'security/ir.model.access.csv',
        'views/crisis_views.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
