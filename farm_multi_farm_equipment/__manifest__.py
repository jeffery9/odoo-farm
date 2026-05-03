{
    'name': 'Multi-Entity Equipment Management',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Multi-Entity Equipment Management Module',
    'description': """
        Equipment management module for Multi-Entity Collaboration System.
        - Shared machinery pool and dynamic settlement [US-19-08]
        - Machinery rental and sharing [US-19-08]
        - Equipment resource scheduling [US-19-03]
    """,
    'author': 'Jeffery',
    'depends': [
        'farm_multi_farm_base',
        'fleet',
        'base',
        'mail',
    ],
    'data': [
        'views/menu.xml',
        'security/ir.model.access.csv',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}