{
    'name': 'Farm POS Integration',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Link Picking Activities to POS Sales',
    'description': """
        POS module for Odoo 19 Farm Management System.
        - Associate POS orders with specific picking plots [US-02-02]
        - Automated stock deduction from land parcels
        - Traceability from Receipt to Field
    """,
    'author': \"genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>\",
    'depends': ['farm_core', 'point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/pos_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
