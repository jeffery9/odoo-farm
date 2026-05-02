{
    'name': 'Multi-Entity Collaboration & Cooperative Management (Base)',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Multi-Entity Collaboration & Cooperative Management Base Module',
    'description': """
        Base module for Multi-Entity Collaboration & Cooperative Management System.
        - Multi-farm entity relationship modeling [US-19-01]
        - Tenant-level data isolation and sharing [US-19-02]
        - Cross-farm resource scheduling and collaboration [US-19-03]
        - Franchise farm standardized management [US-19-05]
        - Cooperative member management [US-19-06]
        - Regional oversight and governance [US-19-17]
    """,
    'author': 'Jeffery',
    'depends': [
        'farm_core',
        'base',
        'mail',
        'contacts',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/entity_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}