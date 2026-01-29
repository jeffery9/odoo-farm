{
    'name': 'Farm Sustainability & Environment',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Sustainability Indicators, Fertilizer Reduction and Ecological Buffers',
    'description': """
        Sustainability module for Odoo 19 Farm Management System.
        - Monitoring Fertilizer (N/P/K) Reduction Trends [US-08-03]
        - Ecological Buffer Zone Maintenance Records
        - Environmental Impact Dashboards
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
        'farm_supply_analytics',
        'farm_esg_compliance',
        'farm_ai_decision'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sustainability_views.xml',
        'views/carbon_views.xml',
        'views/sustainability_metric_views.xml',
        'views/circular_flow_views.xml',
        'views/sustainability_dashboard_views.xml',
        'data/sustainability_data.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
