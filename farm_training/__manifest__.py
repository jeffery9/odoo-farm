{
    'name': 'Farm Training & Certification',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Farmer Skill Training and Mandatory Qualification Checks',
    'description': """
        US-17-08: Farmer training and qualification admission.
        - Training session management and hour tracking.
        - Certificate management with expiry monitoring.
        - Mandatory qualification checks for professional tasks (e.g. Drone, Chemical handling).
    """,
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "website": "http://www.geninit.cn",
    'depends': ['hr', 'farm_core', 'farm_operation'],
    'data': [
        'security/ir.model.access.csv',
        'views/training_views.xml',
        'views/employee_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
