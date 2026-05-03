{
    'name': 'Farm Government Finance (DEPRECATED)',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'DEPRECATED - Use farm_financial_government instead',
    'description': """
        DEPRECATED: Government finance management for rural revitalization projects.

        This module has been deprecated. Use the new specialized module instead:
        - farm_financial_government: Government program management

        Please migrate to the new specialized module for better functionality.
    """,
    'author': 'Jeffery',
    'depends': [
        'account',
        'farm_financial_government',  # Use new specialized module
    ],
    'auto_install': False,  # Don't auto-install deprecated module
    'data': [
        'security/ir.model.access.csv',
        'report/project_fund_report_templates.xml',
        'report/project_fund_reports.xml',
        'views/finance_gov_views.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
