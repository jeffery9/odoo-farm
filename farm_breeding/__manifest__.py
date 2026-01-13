{
    'name': 'Farm Breeding & Nursery',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Nursery Batch Tracking and Breeding Pedigree',
    'description': """
        Breeding module for Odoo 19 Farm Management System.
        - Nursery Factory Management (Seedling Age, Survival Rate) [US-03-02]
        - Pedigree & Trait Tracking [US-10-02]
    """,
    'author': 'Jeffery',
    'depends': ['farm_operation', 'farm_core'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/trait_comparison_wizard_views.xml',
        'views/nursery_batch_views.xml',
        'views/breeding_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
