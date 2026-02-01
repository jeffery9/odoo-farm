{
    'name': 'Winery & Enology Management',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Specialized management for winemaking, fermentation, barrel aging, and blending.',
    'depends': ['farm_core', 'farm_isl', 'farm_processing', 'farm_viticulture'],
    'data': [
        'security/ir.model.access.csv',
        'views/winery_isl_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}
