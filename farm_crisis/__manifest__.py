{
    'name': 'Farm Crisis & Emergency Response',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Emergency Protocols and Crisis Management SOPs',
    'description': """
        Manage agricultural emergencies and crisis response [US-17-03].
        - Emergency Protocols (SOPs for Disease, Fire, Contamination)
        - Crisis Mode Activation & Asset Lockdown
        - Incident Logging & Reporting
    """,
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "website": "http://www.geninit.cn",
    'depends': ['farm_core', 'farm_safety'],
    'data': [
        'security/ir.model.access.csv',
        'views/crisis_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
