{
    'name': "Farm Training",
    'summary': "Manage farmer training, skills, and certifications for farm workers.",
    'description': """
        Module to manage farmer training programs, track employee skills,
        and issue/validate certifications for various agricultural tasks.
        It helps HR manage worker qualifications and prevent unqualified assignments.
    """,
    'author': "Your Company Name",
    'website': "https://www.yourcompany.com",
    'category': 'Human Resources/Farm',
    'version': '1.0',
    'depends': [
        'base',
        'hr', # Dependency on Odoo's Human Resources module for employees
        'farm_core', # Dependency on farm_core for farm-specific base data
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/farm_training_views.xml',
        'views/hr_employee_views.xml',
        'data/farm_training_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}