{
    'name': 'Farm Supply (MIGRATION STATUS ONLY)',
    'version': '19.0.1.0.0',
    'category': 'Industries/Agriculture',
    'summary': 'Migration status documentation only - all functionality moved to specialized modules',
    'description': """
        This module is retained only for migration status documentation.
        All supply functionality has been moved to specialized modules:
        - farm_supply_procurement: Agricultural input management and procurement
        - farm_supply_quality: Quality-based pricing and grading
        - farm_supply_logistics: Cold chain and logistics management
        - farm_supply_analytics: Supply chain analytics and risk monitoring
        - farm_supply_core: Core supply chain infrastructure
    """,
    'author': 'Jeffery',
    'depends': [
        'farm_core',
        'farm_supply_core',
        'farm_supply_procurement',
        'farm_supply_quality',
        'farm_supply_analytics',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
