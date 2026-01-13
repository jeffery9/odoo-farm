{
    'name': 'Farm CSA Subscriptions',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Community Supported Agriculture (CSA) and Weekly Vegetable Bags',
    'description': """
        CSA module for Odoo 19 Farm Management System.
        - Subscription Plan management (Weekly, Monthly) [US-02-04]
        - Automated Delivery Task (Picking) Generation
        - Customer Subscription Lifecycle
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'stock', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/csa_subscription_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
