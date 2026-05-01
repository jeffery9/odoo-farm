{
    'name': 'Farm Circular Economy',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Circular Economy and Resource Flow Models (Epic 27)',
    'description': """
Circular economy module for Odoo 19 Farm Management System - Epic 27 Implementation.
- Circular flow economics and resource utilization optimization
- Waste-to-resource conversion tracking
- Hazardous waste compliance management (US-27-03)
- Biogas and energy recovery quantification (US-27-04)
- Cooperative resource sharing coordination (US-27-05)
- GIS-driven geospatial cycle network (US-27-06)
- Regional circular economy governance (US-27-07)
    """,
    'author': 'Jeffery',
    'depends': [
        'base',
        'mail',
        'farm_core',
        'farm_operation',
        'farm_esg',
         # For integration with ESG compliance
        'product',  # For product references
        'uom',      # For unit of measure
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/circular_flow_views.xml',
        'views/hazardous_waste_views.xml',
        'views/biogas_energy_views.xml',
        'views/cooperative_coordination_views.xml',
        'views/geospatial_coordination_views.xml',
        'views/regional_governance_views.xml',
        'views/menu.xml',
        'data/ir_sequence_data.xml',
        'data/sustainability_data.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}