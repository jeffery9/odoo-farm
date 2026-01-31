{
    'name': 'Farm Sustainability Reporting',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Sustainability Dashboards, Reports and Analytics',
    'description': """
        Sustainability reporting module for Odoo 19 Farm Management System.
        - Sustainability dashboards
        - ESG compliance reports
        - Sustainability metrics and analytics
        - Environmental impact assessment
    """,
    'author': 'Jeffery',
    'depends': [
        'base',
        'mail',
        'board',
        'web',
        'farm_core',
        'farm_operation',
        'farm_financial',
        'farm_esg',
        'farm_esg_carbon',
        'farm_esg_environmental',
        'farm_esg_circular',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sustainability_views.xml',
        'views/sustainability_metric_views.xml',
        'views/sustainability_dashboard_views.xml',
        'data/sustainability_data.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}