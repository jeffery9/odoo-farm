{
    'name': 'Farm Breeding & Nursery',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Nursery Batch Tracking and Breeding Pedigree',
    'description': """
        Breeding module for Odoo 19 Farm Management System.
        - Nursery Factory Management (Seedling Age, Survival Rate) [US-31]
        - Pedigree & Trait Tracking [US-32]
    """,
    'author': 'Jeffery',
    'depends': ['farm_operation', 'farm_core'],
    'data': [
        'security/ir.model.access.csv',
        'views/nursery_batch_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
