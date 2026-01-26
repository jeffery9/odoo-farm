{
    'name': 'Farm Finance & Loans',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Agricultural Loans, Collateral Valuation and Credit Lines',
    'description': """
        Financial management for agricultural loans and credit [US-17-04].
        - Biological Asset Valuation for Collateral
        - Loan Application & Repayment Schedules
        - Integration with Production Cycles
    """,
    'author': 'Jeffery',
    'depends': ['farm_operation', 'farm_financial'],
    'data': [
        'security/ir.model.access.csv',
        'views/finance_loan_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
