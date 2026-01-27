{
    'name': 'Farm Agricultural Science & VRA',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Scientific Trial Management & Variable Rate Application (VRA) Engine',
    'description': """
        Agricultural science and Precision VRA module.
        - Variable Rate Application (VRA) Engine [Epic 46]
        - Land Parcel Grid Management (5x5m mapping)
        - NDVI/Soil Data Integration for Prescription Maps
        - ISO-XML & Shapefile Export Interface for Machinery
        - Scientific trial management and experimental design
        - Biological Digital Twin & AI Yield Prediction [L3]
    """,
    'author': 'genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>',
    'website': 'http://www.geninit.cn',
    'depends': ['farm_core', 'farm_operation', 'farm_iot'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/land_grid_views.xml',
        'views/vra_strategy_views.xml',
        'views/vra_prescription_views.xml',
        'views/biological_twin_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}