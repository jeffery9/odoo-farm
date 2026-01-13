{
    'name': 'Farm Financials & Costs',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Farm Cost Accounting and Financial Dashboards',
    'description': """
        Financial module for Odoo 19 Farm Management System.
        - Comprehensive Cost Accounting (Inputs, Labor, Overhead) [US-04-02]
        - Automated Cost Attribution to Plots/Lots/Campaigns
        - Profitability Analysis per Production Unit
        - Storage and Processing Cost Allocation [US-14-13]
    """,
    'author': \"genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>\",
    'depends': ['farm_operation', 'account', 'analytic'],
    'data': [
        'security/ir.model.access.csv',
        'data/analytic_data.xml',
        'views/farm_cost_analysis_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
