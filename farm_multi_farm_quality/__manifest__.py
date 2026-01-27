{
    'name': 'Multi-Entity Quality Management',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Multi-Entity Quality Management Module',
    'description': """
        Quality management module for Multi-Entity Collaboration System.
        - Cooperative quality control and brand access [US-19-09]
        - Product certification management [US-19-09]
        - Quality standard compliance [US-19-09]
    """,
    'author': 'Jeffery',
    'depends': [
        'farm_multi_farm_base',
        'quality',
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/quality_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}