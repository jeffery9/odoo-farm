{
    'name': 'Farm Operation',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Production Seasons, Tasks and Agri-Interventions',
    'description': """
        Operation engine for Odoo 19 Farm Management System.
        - Production Season Planning (Campaign) [US-05]
        - Agri-Intervention Records (Interventions) [US-06]
        - Harvest & Grading [US-08]
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'mrp', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'views/agricultural_campaign_views.xml',
        'views/farm_production_task_views.xml',
        'views/agri_intervention_views.xml',
        'views/agri_bom_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
