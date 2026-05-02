{
    'name': 'Seed Industry & R&D Management',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Specialized management for seed breeding, propagation, testing (Germination/Purity), and PVP compliance.',
    'depends': ['farm_core', 'farm_isl', 'farm_breeding', 'farm_agricultural_processing'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/seed_isl_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}
