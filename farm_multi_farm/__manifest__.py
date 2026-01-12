{
    'name': 'Farm Multi-Farm & Cooperative',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Multi-Farm / Cooperative Collaboration and Resource Sharing',
    'description': """
        Enables collaboration between multiple farms or cooperative members [US-17-09].
        - Cross-company resource scheduling (machinery, personnel).
        - Internal settlement mechanisms for shared resources.
        - Unified management for group-owned assets.
    """,
    'author': 'Jeffery',
    'depends': ['base', 'farm_core', 'farm_equipment', 'farm_hr', 'farm_logistics', 'project', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/multi_farm_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}