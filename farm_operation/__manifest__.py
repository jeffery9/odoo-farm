{
    'name': 'Farm Operation',
    'version': '1.2.1',
    'category': 'Industries/Agriculture',
    'summary': 'Multi-Industry Farm Operations with Agri-Science Synchronization',
    'description': """
        Multi-Industry Operation Engine for Odoo 19 Farm Management System.

        Features:
        - Production Season Planning (Campaign) [US-056-01] with industry adaptability
        - Agri-Intervention Records (Interventions) [US-002-02] for different industries
        - Harvest & Grading [US-002-04] with industry-specific variants
        - Product Grading and Batch Management [US-037-05] for multiple sectors
        - Industry-specific task types and parameterization
        - Support for multiple agricultural sectors (field crops, livestock, aquaculture, etc.)
        - Flexible operation definitions adaptable to different farming practices
        - [US-045-09] Scientific Performance Dashboard (RUE/WUE)
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'farm_agri_science', 'mrp', 'project', 'farm_ux', 'sale', 'agri_iot'],
    'data': [
        # 'security/ir.model.access.csv',
        'wizard/farm_dispatch_wizard_views.xml',
        'wizard/agri_science_sync_wizard_views.xml',
        'views/menu.xml',
        'views/agricultural_campaign_views.xml',
        'views/project_task_views.xml',
        'views/agri_intervention_views.xml',
        'views/agri_science_dashboard_views.xml',
        'views/agri_bom_views.xml',
    ],
    'demo': [
        'data/farm_operation_demo.xml',
    ],
    
    'assets': {
        'web.assets_tests': [
            'farm_operation/static/tests/tours/**/*',
        ],
    },
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}