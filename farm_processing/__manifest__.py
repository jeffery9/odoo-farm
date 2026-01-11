{
    'name': 'Farm Processing',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Agricultural Product Processing and Energy Tracking',
    'description': """
        Processing module for Odoo 19 Farm Management System.
        - Agri-Processing Orders (Linked to Raw Material Lots)
        - Energy & Resource Consumption Tracking [US-62]
        - Forward and Backward Traceability (Field to Table)
        - Support for By-products (US-44 One-in, Many-out)
    """,
    'author': 'Jeffery',
    'depends': ['farm_operation', 'mrp'],
    'data': [
        'security/ir.model.access.csv',
        'data/processing_data.xml',
        'views/farm_processing_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
