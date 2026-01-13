{
    'name': 'Farm Operation',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Production Seasons, Tasks and Agri-Interventions',
    'description': """
        Operation engine for Odoo 19 Farm Management System.
        - Production Season Planning (Campaign) [US-01-02]
        - Agri-Intervention Records (Interventions) [US-02-02]
        - Harvest & Grading [US-02-04]
        - Product Grading and Batch Management [US-14-05]
    """,
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "website": "http://www.geninit.cn",
    'depends': ['farm_core', 'mrp', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'views/agricultural_campaign_views.xml',
        'views/project_task_views.xml',
        'views/agri_intervention_views.xml',
        'views/agri_bom_views.xml',
    ],
    'demo': [
        'data/farm_operation_demo.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
