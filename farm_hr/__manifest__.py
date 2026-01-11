{
    'name': 'Farm HR & Labor',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Seasonal Labor, Field Worklogs and Piece-rate Wages',
    'description': """
        HR module for Odoo 19 Farm Management System.
        - Seasonal Labor Management (Contractors/External workers) [US-42]
        - Field Task Worklogs & Piece-rate performance [US-43]
        - Automated labor cost attribution to farm tasks
    """,
    'author': 'Jeffery',
    'depends': ['farm_operation', 'hr', 'hr_attendance', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/farm_employee_views.xml',
        'views/farm_worklog_views.xml',
        'views/farm_wage_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
