{
    'name': 'Farm Logistics (DEPRECATED)',
    'version': '19.0.1.0.0',
    'category': 'Industries/Agriculture',
    'summary': 'DEPRECATED - Use farm_supply_logistics module instead',
    'description': """
        DEPRECATED: Logistics module for Odoo 19 Farm Management System.

        This module has been deprecated. Logistics functionality is now available
        in the farm_supply_logistics module which provides cold chain management,
        packaging support, and integrated field delivery.

        Please use farm_supply_logistics for all logistics related functionality.
    """,
    'author': 'Jeffery',
    'depends': [
        'farm_core',
        'farm_supply_core',
        'farm_supply_logistics',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
