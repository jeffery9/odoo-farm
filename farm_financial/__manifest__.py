{
    'name': 'Farm Financials & Costs',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Farm Cost Accounting and Financial Dashboards',
    'description': """
        Financial module for Odoo 19 Farm Management System.
        - Comprehensive Cost Accounting (Inputs, Labor, Overhead) [US-41]
        - Automated Cost Attribution to Plots/Lots/Campaigns
        - Profitability Analysis per Production Unit
    """,
    'author': 'Jeffery',
    'depends': ['farm_operation', 'account', 'analytic'],
    'data': [
        'security/ir.model.access.csv',
        'data/analytic_data.xml',
        'views/farm_cost_analysis_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
