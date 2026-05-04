{
    'name': 'Multi-Entity Financial Management',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Multi-Entity Financial Management Module',
    'description': """
        Financial management module for Multi-Entity Collaboration System.
        - Member shares and dividend management [US-042-06]
        - Internal credit and lending management [US-042-07]
        - Dividend distribution and tracking [US-042-06]
        - Share transaction recording [US-042-06]
    """,
    'author': 'Jeffery',
    'depends': [
        'farm_multi_farm_base',
        'account',
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