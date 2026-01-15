{
    'name': 'Farm MRP Base (ISL Infrastructure)',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Base infrastructure for Industry Specialized Layer (ISL) on MRP models',
    'description': """
        This module provides the base Mixins and redirection logic for agricultural 
        Industry Specialized Layer (ISL) implementation on top of Odoo MRP.

        It follows the "Delegation Inheritance" pattern to allow multiple agricultural 
        verticals (Livestock, Crop, Processing) to coexist on the same Odoo base.
    """,
    'author': 'Jeffery',
    'depends': ['mrp', 'stock', 'farm_core'],
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}