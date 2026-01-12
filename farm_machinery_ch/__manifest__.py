{
    'name': 'Farm Machinery Subsidy (China)',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'China-specific Agricultural Machinery Purchase Subsidy Management',
    'description': """
        Supports Chinese government's agricultural machinery purchase subsidy policies [US-71].
        - Automatic matching with national subsidy catalogs based on machinery specifications.
        - Pre-fills application fields (e.g., category, grading parameters).
        - Generates subsidy application packages including invoices, photos, and usage proofs.
    """,
    'author': 'Jeffery',
    'depends': ['farm_equipment', 'farm_core'],
    'data': [
        'security/ir.model.access.csv',
        'report/machinery_subsidy_report_templates.xml',
        'report/machinery_subsidy_reports.xml',
        'views/machinery_subsidy_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
