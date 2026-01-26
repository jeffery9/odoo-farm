{
    'name': 'Farm Operation',
    'version': '1.1',
    'category': 'Industries/Agriculture',
    'summary': 'Multi-Industry Farm Operations - Production Seasons, Tasks, Agri-Interventions with Industry Adaptability',
    'description': """
        Multi-Industry Operation Engine for Odoo 19 Farm Management System.

        Features:
        - Production Season Planning (Campaign) [US-01-02] with industry adaptability
        - Agri-Intervention Records (Interventions) [US-02-02] for different industries
        - Harvest & Grading [US-02-04] with industry-specific variants
        - Product Grading and Batch Management [US-14-05] for multiple sectors
        - Industry-specific task types and parameterization
        - Support for multiple agricultural sectors (field crops, livestock, aquaculture, etc.)
        - Flexible operation definitions adaptable to different farming practices
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'mrp', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/farm_dispatch_wizard_views.xml',
        'views/agricultural_campaign_views.xml',
        'views/project_task_views.xml',
        'views/agri_intervention_views.xml',
        'views/agri_bom_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'data/farm_operation_demo.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
