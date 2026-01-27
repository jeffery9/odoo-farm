{
    'name': 'Farm Multi-Entity Collaboration & Cooperative Management',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Multi-Entity Collaboration & Cooperative Management',
    'description': """
        Multi-Entity Collaboration & Cooperative Management Module for Odoo 19 Farm Management System.
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
        - "Company + Farmer" contract farming management [US-19-24]
    """,
    'author': 'Jeffery',
    'depends': [
        'farm_core',
        'farm_multi_farm_base',
        'farm_multi_farm_financial',
        'farm_multi_farm_procurement',
        'farm_equipment',
        'farm_hr',
        'farm_financial',
        'farm_marketing',
        'project',
        'account',
        'farm_agri_science',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/multi_farm_data.xml',
        'views/entity_views.xml',
        'views/member_share_views.xml',
        'views/quality_operations_views.xml',
        'views/finance_governance_views.xml',
        'views/advanced_procurement_views.xml',
        'views/regional_oversight_views.xml',
        'views/stock_lot_views.xml',
        'views/contract_farming_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
