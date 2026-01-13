{
    'name': 'Farm Waste Management (China)',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'China-specific Livestock/Poultry Manure Management and Ledger',
    'description': """
        Manages livestock and poultry manure resource utilization ledgers [US-18-05].
        - Records disposal methods (composting, biogas, third-party transfer).
        - Tracks destination and recipient information.
        - Generates monthly ledgers compliant with Ministry of Agriculture and Rural Affairs requirements.
        - Processing Waste Registration [US-14-12]
    """,
    'author': \"genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>\",
    'depends': ['farm_core', 'farm_livestock'],
    'data': [
        'security/ir.model.access.csv',
        'report/manure_ledger_report_templates.xml',
        'report/manure_ledger_reports.xml',
        'views/waste_mgmt_views.xml',
        'views/waste_management_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
