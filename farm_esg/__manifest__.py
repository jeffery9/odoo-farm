{
    'name': 'Farm ESG Management',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Environmental, Social and Governance Management for Farm Operations',
    'description': """
ESG Management Module for Odoo 19 Farm Management System.
- Environmental compliance and reporting [US-56-01]
- Social responsibility and community impact tracking [US-56-02]
- Governance and risk management [US-56-03]
- ESG data governance and audit trails [US-56-04]
- ESG reporting and dashboard [US-56-05]
""",
    'author': 'Jeffery',
    'depends': [
        'base',
        'farm_core',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/esg_framework_views.xml',
        'views/esg_indicator_views.xml',
        'views/esg_target_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}