{
    'name': 'Farm Input Regulation (China)',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'China-specific Pesticide/Veterinary Drug Real-name Registration',
    'description': """
        Implements China's regulations on agricultural input usage [US-10-02].
        - Real-name registration for pesticide/veterinary drug applicators.
        - Tracking of product registration numbers.
        - Warning/Blocking for prohibited/restricted inputs.
        - Simulation of data synchronization to provincial regulatory platforms.
    """,
    'author': 'Jeffery',
    'depends': ['farm_supply', 'farm_operation'],
    'data': [
        'security/ir.model.access.csv',
        'views/input_reg_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
