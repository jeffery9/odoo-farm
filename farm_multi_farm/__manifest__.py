{
    'name': 'Farm Multi-Entity Collaboration & Cooperative Management',
    'version': '1.2.0',
    'category': 'Industries/Agriculture',
    'summary': 'Multi-Entity Collaboration, Cooperative Management & Cross-Farm Governance',
    'description': """
        Multi-Entity Collaboration & Cooperative Management Module for Odoo 19 Farm Management System.
        (Consolidated from farm_multi_farm and farm_multi_farm)
        
        Core Features:
        - Multi-farm entity relationship modeling [US-042-01]
        - Tenant-level data isolation and sharing [US-042-02]
        - Cooperative-level financial consolidation [US-042-04]
        - Franchise farm standardized management [US-042-05]
        - Member shares and dividend management [US-042-06]
        - Internal marketplace and resource sharing [US-042-11]
        - Regional oversight and governance [US-042-17]
    """,
    'author': 'Jeffery',
    'depends': [
        'base',
        'mail',
        'contacts',
        'farm_core',
        'project',
        'account',
        'farm_agri_science',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule_lot.xml',
        'data/multi_farm_data.xml',
        'views/entity_views.xml',
        'views/regional_oversight_views.xml',
        'views/stock_lot_views.xml',
        'views/menu.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}
