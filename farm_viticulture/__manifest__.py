{
    'name': 'Viticulture & Vineyard Management',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Specialized management for vineyards, wine grape production, and terroir tracking.',
    'depends': ['farm_core', 'farm_isl', 'farm_operation', 'farm_agricultural_processing'],
    'data': [
        'security/ir.model.access.csv',
        'views/viticulture_isl_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}
