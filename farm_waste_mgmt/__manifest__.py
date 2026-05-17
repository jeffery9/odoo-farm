{
    'name': 'Farm Waste Management (China)',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'China-specific Livestock/Poultry Manure Management and Ledger',
    'description': """
        Manages livestock and poultry manure resource utilization ledgers [US-041-05].
        - Records disposal methods (composting, biogas, third-party transfer).
        - Tracks destination and recipient information.
        - Generates monthly ledgers compliant with Ministry of Agriculture and Rural Affairs requirements.
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'farm_livestock', 'farm_quality'],
    'data': [
        'security/ir.model.access.csv',
        'report/manure_ledger_report_templates.xml',
        'report/manure_ledger_reports.xml',
        'views/waste_mgmt_views.xml',
        'views/waste_management_views.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
