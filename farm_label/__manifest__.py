{
    'name': 'Farm Labels & Signage',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Printable labels for products, lots, animals and land parcels',
    'description': """
        Labeling module for Odoo 19 Farm Management System.
        - Consumer Product Labels with Traceability QR [US-08-01]
        - Internal Batch/Lot Tags
        - Individual Animal Identification (Ear Tags) [US-01-04]
        - Land Parcel Signage with GIS/History QR [US-01-03]
        - Package Conversion and Label Compliance [US-14-10]
    """,
    'author': \"genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>\",
    'depends': ['farm_core', 'farm_marketing', 'barcodes'],
    'data': [
        'report/farm_label_templates.xml',
        'report/farm_label_reports.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
