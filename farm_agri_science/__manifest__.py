{
    'name': 'Farm Agri-Science Foundation',
    'version': '1.1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Growth Models, Physiology Fingerprints & Variable Rate Application (VRA) Engine',
    'description': """
        [US-201] [ISA-88] Core Agricultural Science Foundation.
        - Variety Physiology Fingerprint Management (T-base, T-opt, T-max).
        - Physiological Stage & GDD (Growing Degree Days) Mapping.
        - Biological Stress Integral Calculation.
        - Resource Use Efficiency (RUE/WUE) Framework.
        - Variable Rate Application (VRA) Engine [Epic 46]
        - Land Parcel Grid Management (5x5m mapping)
    """,
    'author': 'genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>',
    'website': 'http://www.geninit.cn',
<<<<<<< HEAD
    'depends': ['farm_core'],
=======
    'depends': ['farm_core', 'mrp'],
>>>>>>> 5351cad217860264bdd3ca8394fa45a799fce3d0
    'data': [
        # 'security/ir.model.access.csv',
        # 'data/ir_sequence_data.xml',
        'views/physiology_profile_views.xml',
        'views/growth_stage_views.xml',
        'views/land_grid_views.xml',
        'views/vra_strategy_views.xml',
        'views/vra_prescription_views.xml',
        'views/biological_twin_views.xml',
        'views/menu.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}