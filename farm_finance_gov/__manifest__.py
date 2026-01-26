{
    'name': 'Farm Government Finance (China)',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'China-specific Financial Accounting for Rural Revitalization Projects',
    'description': """
        Manages dedicated accounting for government-supported rural revitalization project funds [US-18-09].
        - Associates purchase and expense documents with specific project numbers.
        - Generates detailed project fund utilization reports with invoice references.
        - Ensures dedicated use of special funds.
    """,
    'author': 'Jeffery',
    'depends': ['account', 'farm_financial'],
    'data': [
        'security/ir.model.access.csv',
        'report/project_fund_report_templates.xml',
        'report/project_fund_reports.xml',
        'views/finance_gov_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
