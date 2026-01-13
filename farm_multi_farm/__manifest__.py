{
    'name': 'Farm Multi-Entity Collaboration & Cooperative Management',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Multi-Entity Collaboration & Cooperative Management',
    'description': """
        Multi-Entity Collaboration & Cooperative Management Module for Odoo 19 Farm Management System.
        
        Features:
        - Multi-farm entity relationship modeling [US-19-01]
        - Tenant-level data isolation and sharing [US-19-02]
        - Cross-farm resource scheduling and collaboration [US-19-03]
        - Cooperative-level financial consolidation and cost allocation [US-19-04]
        - Franchise farm standardized management [US-19-05]
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'farm_equipment', 'farm_hr', 'farm_financial', 'farm_marketing', 'project', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'data/multi_farm_data.xml',
        'views/multi_farm_views.xml',
        'views/menu.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}