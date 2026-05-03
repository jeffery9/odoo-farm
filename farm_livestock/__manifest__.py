{
    'name': 'Farm Livestock',
    'version': '1.2',
    'category': 'Industries/Agriculture',
    'summary': 'Livestock Management - Breeding Records, Health Records, Breeding Management, Individual Identification',
    'description': """
        Livestock Management Module for Odoo 19 Farm Management System.

        Features:
        - Individual animal identification and tracking [US-64-01]
        - Breeding records and pedigree management [US-64-04]
        - Health records and veterinary tracking [US-64-10]
        - Smart Health Monitoring & Anomalies [US-64-02]
        - House Environment Tracking [US-64-05]
        - Feeding Plans & Formulas (BOM based) [US-64-03, US-64-09]
        - Group Movements (Merge, Split, Death) [US-05-04]
        - Animal lifecycle and age-based management [US-64-01]
    """,
    'author': 'Jeffery',
    'depends': ['farm_operation', 'farm_core', 'farm_mrp', 'project', 'mrp', 'stock'],
    'data': [
        # 'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/livestock_lot_views.xml',
        'views/livestock_advanced_views.xml',
        'views/livestock_feeding_views.xml',
        'views/livestock_events_views.xml',
        'views/livestock_views.xml',
        'views/livestock_isl_views.xml',
        'views/updated_livestock_production_view.xml',
        'views/menu.xml',
    ],
    'demo': [
        'data/farm_livestock_demo.xml',
    ],
    
    'assets': {
        'web.assets_tests': [
            'farm_livestock/static/tests/tours/**/*',
        ],
    },
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}