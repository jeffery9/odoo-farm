{
    'name': 'Farm Multi-Farm & Cooperative',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Multi-Farm / Cooperative Collaboration and Resource Sharing',
    'description': """
        Multi-entity collaboration and cooperative management module for Odoo 19 Farm Management System.
        - Multi-farm entity relationship modeling [US-19-01]
        - Tenant-level data isolation and sharing [US-19-02]
        - Cross-farm resource scheduling and collaboration [US-19-03]
        - Cooperative-level financial consolidation and allocation [US-19-04]
        - Franchise farm standardized management [US-19-05]
        - Cross-company resource scheduling (machinery, personnel).
        - Internal settlement mechanisms for shared resources.
        - Unified management for group-owned assets.
    """,
    'author': 'Jeffery',
    'depends': ['base', 'farm_core', 'farm_equipment', 'farm_hr', 'farm_logistics', 'project', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/multi_farm_views.xml',
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}