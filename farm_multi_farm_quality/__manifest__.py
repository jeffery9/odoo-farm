{
    'name': 'Multi-Entity Quality Management',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Multi-Entity Quality Management Module',
    'description': """
        Quality management module for Multi-Entity Collaboration System.
        - Cooperative quality control and brand access [US-042-09]
        - Product certification management [US-042-09]
        - Quality standard compliance [US-042-09]
    """,
    'author': 'Jeffery',
    'depends': [
        'farm_multi_farm_base',
        'farm_quality',
        'base',
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