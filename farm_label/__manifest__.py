{
    'name': 'Farm Labels & Signage',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Printable labels for products, lots, animals and land parcels',
    'description': """
        Labeling module for Odoo 19 Farm Management System.
        - Consumer Product Labels with Traceability QR [US-25]
        - Internal Batch/Lot Tags
        - Individual Animal Identification (Ear Tags) [US-04]
        - Land Parcel Signage with GIS/History QR [US-03]
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'farm_marketing', 'barcodes'],
    'data': [
        'report/farm_label_templates.xml',
        'report/farm_label_reports.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
