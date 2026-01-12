{
    'name': 'Farm Processing',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Agricultural Product Processing and Energy Tracking',
    'description': """
        Processing module for Odoo 19 Farm Management System.
        - Agri-Processing Orders (Linked to Raw Material Lots) [US-14-01, US-14-02]
        - Energy & Resource Consumption Tracking [US-17-08, US-14-04]
        - Forward and Backward Traceability (Field to Table) [US-14-03]
        - Support for By-products (US-04-02 One-in, Many-out) [US-14-08]
        - Batch Management and Grading [US-14-05]
        - Storage Environment Monitoring [US-14-06]
        - Product Loss Management [US-14-07]
        - Multi-level Recipe Management [US-14-09]
        - Package Conversion and Label Compliance [US-14-10]
        - Cold Chain Logistics [US-14-11]
        - Waste Registration [US-14-12]
        - Cost Allocation [US-14-13]
        - Expiry Warning and Promotion [US-14-14]
    """,
    'author': 'Jeffery',
    'depends': ['farm_operation', 'mrp'],
    'data': [
        'security/ir.model.access.csv',
        'data/processing_data.xml',
        'views/farm_processing_views.xml',
    ],
    'demo': [
        'data/farm_processing_demo.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
