{
    'name': 'Multi-Entity Procurement Management',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Multi-Entity Procurement Management Module',
    'description': """
        Procurement management module for Multi-Entity Collaboration System.
        - Joint procurement and internal clearing [US-19-10]
        - Procurement planning and allocation [US-19-12]
        - Internal marketplace for resource sharing [US-19-11]
    """,
    'author': 'Jeffery',
    'depends': [
        'farm_multi_farm_base',
        'purchase',
        'stock',
        'base',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}