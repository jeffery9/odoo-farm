{
    'name': 'Multi-Entity Procurement Management',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Multi-Entity Procurement Management Module',
    'description': """
        Procurement management module for Multi-Entity Collaboration System.
        - Joint procurement and internal clearing [US-042-10]
        - Procurement planning and allocation [US-042-12]
        - Internal marketplace for resource sharing [US-042-11]
    """,
    'author': 'Jeffery',
    'depends': [
        'farm_multi_farm',
        'purchase',
        'stock',
        'base',
        'mail',
    ],
    'data': [
        'views/menu.xml',
        #'security/ir.model.access.csv',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}