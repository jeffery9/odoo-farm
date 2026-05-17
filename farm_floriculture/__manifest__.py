{
    'name': 'Floriculture & Ornamental Horticulture',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Specialized management for flower production, bloom control, and vase-life tracking.',
    'description': """
Floriculture Module (ISL Implementation)
- Manual flowering control (lighting/temp) [US-FLOR-01]
- Extreme cold-chain monitoring integration [US-FLOR-02]
- Vase-life prediction and quality grading [US-FLOR-03]
""",
    'author': 'Jeffery',
    'depends': [
        'farm_core',
        'farm_isl',
        'farm_operation',
    ],
    'data': [
        #'security/ir.model.access.csv',
        'views/flower_isl_views.xml',
        'views/menu.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}
