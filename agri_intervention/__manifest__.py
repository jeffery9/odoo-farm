# -*- coding: utf-8 -*-
{
    'name': 'Agri Intervention Engine (Core)',
    'version': '1.0.0',
    'category': 'Industries/Agriculture',
    'summary': 'Standardized Agricultural Intervention Engine (ISA-95 compliant)',
    'description': """
        Foundational Engine for Agricultural Interventions. [L0 Foundation]
        
        - Pure abstraction for any biological or physical farm action.
        - Decoupled from Odoo's business applications (MRP/Task).
        - Plugin-based architecture for weather gating, spatial audit, and resource tracking.
        - Standardized lifecycle management for farm operations.
    """,
    'author': 'Jeffery',
    'depends': ['farm_core'],
    'data': [
        'security/ir.model.access.csv',
        'views/intervention_base_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}
