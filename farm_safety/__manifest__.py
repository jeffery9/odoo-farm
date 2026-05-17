{
    'name': 'Farm Biosafety & Prevention',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Epidemic Prevention Scheduling and Biosafety Control',
    'description': """
        Safety module for Odoo 19 Farm Management System.
        - Automatic Prevention & Plant Protection Scheduling [US-003-03]
        - Quarantine & Outbreak Management [US-031-02]
        - Medicine Withdrawal Period Tracking [US-031-03]
    """,
    'author': 'Jeffery',
    'depends': ['farm_operation', 'farm_core'],
    'data': [
        'security/ir.model.access.csv',
        'views/prevention_template_views.xml',
        'views/project_task_views.xml',
        'views/farm_lot_views.xml',
        'views/biosafety_access_views.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
