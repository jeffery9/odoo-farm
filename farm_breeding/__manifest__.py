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
    'author': \"genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>\",
    'depends': ['farm_operation', 'farm_core'],
    'data': [
        'security/ir.model.access.csv',
        'views/nursery_batch_views.xml',
        'views/breeding_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
