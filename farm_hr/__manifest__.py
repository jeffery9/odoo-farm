{
    'name': 'Farm HR & Labor',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Seasonal Labor, Field Worklogs and Piece-rate Wages',
    'description': """
        HR module for Odoo 19 Farm Management System.
        - Seasonal Labor Management (Contractors/External workers) [US-13-03]
        - Field Task Worklogs & Piece-rate performance [US-13-04]
        - Automated labor cost attribution to farm tasks
    """,
    'author': 'Jeffery',
    'depends': ['farm_operation', 'hr', 'hr_attendance', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'data/farm_hr_data.xml',
        'data/farm_wage_rules_data.xml',
        'views/farm_employee_views.xml',
        'views/farm_worklog_views.xml',
        'views/farm_wage_views.xml',
        'views/farm_training_views.xml', # Add farm_training views here
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
