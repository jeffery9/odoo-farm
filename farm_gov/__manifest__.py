# -*- coding: utf-8 -*-
{
    'name': 'Farm Government Regulatory Bridge',
    'version': '1.0.0',
    'category': 'Industries/Agriculture',
    'summary': 'Regulatory Interface, Automated Reporting & Government Data Support',
    'description': """
        Bridge module for Government Oversight and Regulatory Compliance.
        
        - [US-GOV-01] Immutable Audit Snapshots for interventions.
        - [US-GOV-02] Automated Provincial Platform reporting (Pesticide/Fertilizer).
        - [US-GOV-03] Regional Oversight Dashboard for Agriculture Bureau.
        - [US-GOV-04] Smart Subsidy verification based on GEP and Spatial Compliance.
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'farm_operation', 'farm_input_reg', 'farm_ecology', 'farm_multi_farm'],
    'data': [
        'security/ir.model.access.csv',
        'data/gov_reporting_data.xml',
        'views/gov_audit_views.xml',
        'views/menu.xml',
        'views/gov_platform_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}
