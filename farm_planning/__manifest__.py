{
    'name': 'Farm Planning & Scenarios',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Advanced Production Planning, Technical Routes and Scenarios (Inspired by Ekylibre)',
    'description': """
        Strategic and tactical planning for Odoo 19 Farm Management.
        - Technical Routes (Sequences of intervention templates)
        - Scenario Simulation (What-if analysis)
        - Intervention Proposals (Estimated future tasks)
        - Resource Load Forecasting (Labor, Equipment, Inputs)
    """,
    'author': 'Jeffery',
    'depends': ['farm_operation', 'farm_hr'],
    'data': [
        'security/ir.model.access.csv',
        'data/agri_templates_data.xml',
        'views/intervention_template_views.xml',
        'views/technical_route_views.xml',
        'views/scenario_views.xml',
    ],
    'demo': [
        'data/farm_planning_demo.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}