{
    'name': 'Farm Sale China Export Compliance',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'China-specific Export Compliance and Cross-border Sales',
    'description': """
        Export compliance module for Odoo 19 Farm Management System.
        - Maintain prohibited pesticide lists for different countries [US-17-06]
        - Automatic verification of batch history against destination standards before sales out
        - Generate compliance certificates for export
    """,
    'author': \"genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>\",
    'depends': ['farm_core', 'sale', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'data/export_standards_data.xml',
        'views/export_compliance_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}