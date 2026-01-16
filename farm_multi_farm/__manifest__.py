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
        - Member shares and dividend management [US-19-06]
        - Internal credit and lending management [US-19-07]
        - Shared machinery pool and dynamic settlement [US-19-08]
        - Cooperative quality control and brand access [US-19-09]
        - Joint procurement and internal clearing [US-19-10]
        - Internal marketplace for resource调剂 [US-19-11]
        - Procurement planning and allocation [US-19-12]
        - Agricultural service sharing [US-19-13]
        - Cooperative treasury dashboard [US-19-14]
        - Internal loan and interest calculation [US-19-15]
        - Subsidy disbursement tracking [US-19-16]
        - Governance decision logging [US-19-17]
        - Multi-sign approval processes [US-19-18]
        - Decision audit integration [US-19-19]
        - Virtual procurement consolidation [US-19-20]
        - Hub-and-spoke distribution tracking [US-19-21]
        - Netting settlement for internal transactions [US-19-22]
    """,
    'author': 'Jeffery',
    'depends': [
        'farm_core',      # Core farm infrastructure
        'farm_equipment', # Equipment management for machinery sharing
        'farm_hr',        # Human resources for member management
        'farm_financial', # Financial management infrastructure
        'farm_marketing', # Marketing integration
        'project',        # Project management for service orders
        'account',        # Accounting for settlements and financial records
    ],
    'data': [
        # Security and access rights
        'security/ir.model.access.csv',

        # Data files
        'data/multi_farm_data.xml',

        # Views organized by functionality
        'views/multi_farm_views.xml',           # Basic entity models (farm.entity, cooperative.entity)
        'views/cooperative_shares_views.xml',   # Share and dividend management
        'views/cooperative_operations_views.xml', # Operations and services
        'views/cooperative_finance_views.xml',    # Financial settlements
        'views/menu.xml',                       # Main menu structure
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}