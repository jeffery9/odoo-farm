{
    'name': 'Farm Multi-Entity Collaboration & Cooperative Management',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Multi-Entity Collaboration & Cooperative Management',
    'description': """
        Multi-Entity Collaboration & Cooperative Management Module for Odoo 19 Farm Management System.
        - Multi-farm entity relationship modeling [US-042-01]
        - Tenant-level data isolation and sharing [US-042-02]
        - Cross-farm resource scheduling and collaboration [US-042-03]
        - Cooperative-level financial consolidation and cost allocation [US-042-04]
        - Franchise farm standardized management [US-042-05]
        - Member shares and dividend management [US-042-06]
        - Internal credit and lending management [US-042-07]
        - Shared machinery pool and dynamic settlement [US-042-08]
        - Cooperative quality control and brand access [US-042-09]
        - Joint procurement and internal clearing [US-042-10]
        - Internal marketplace for resource调剂 [US-042-11]
        - Procurement planning and allocation [US-042-12]
        - Agricultural service sharing [US-042-13]
        - Cooperative treasury dashboard [US-042-14]
        - Internal loan and interest calculation [US-042-15]
        - Subsidy disbursement tracking [US-042-16]
        - Governance decision logging [US-042-17]
        - Multi-sign approval processes [US-042-18]
        - Decision audit integration [US-042-19]
        - Virtual procurement consolidation [US-042-20]
        - Hub-and-spoke distribution tracking [US-042-21]
        - Netting settlement for internal transactions [US-042-22]
        - "Company + Farmer" contract farming management [US-042-24]
    """,
    'author': 'Jeffery',
    'depends': [
        'farm_core',
        'farm_multi_farm_base',
        'farm_multi_farm_financial',
        'farm_multi_farm_procurement',
        'farm_equipment',
        'farm_hr',
        'farm_financial_core',
        'farm_marketing',
        'project',
        'account',
        'farm_agri_science',
    ],
    'data': [
        'views/menu.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}