{
    'name': 'Farm Supply & Inputs (DEPRECATED)',
    'version': '19.0.1.0.0',
    'category': 'Industries/Agriculture',
    'summary': 'DEPRECATED - Use specialized supply modules instead',
    'description': """
        DEPRECATED: Supply module for Odoo 19 Farm Management System.

        This module has been deprecated in favor of specialized supply modules:
        - farm_supply_procurement: Agricultural input management and procurement
        - farm_supply_quality: Quality-based pricing and grading
        - farm_supply_logistics: Cold chain and logistics management
        - farm_supply_analytics: Supply chain analytics and risk monitoring
        - farm_supply_core: Core supply chain infrastructure

        Please migrate to the new specialized modules for better functionality and maintenance.
    """,
    'author': 'Jeffery',
    'depends': [
        'farm_core',
        'farm_supply_core',
        'farm_supply_procurement',
        'farm_supply_quality',
        'farm_supply_logistics',
        'farm_supply_analytics',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
