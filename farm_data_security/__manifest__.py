{
    'name': 'Farm Data Security',
    'version': '1.2',
    'category': 'Industries/Agriculture',
    'summary': 'Agricultural Data Security, Localization and Audit',
    'description': """
        Epic 18 & 55: Agricultural Data Security and Compliance.

        Features:
        - Data localization and storage region configuration [US-18-10]
        - Dengbao Level 3 compliance tracking
        - Sensitive operation audit logs (Land deletion, Farmer info modification) [US-18-10]
        - Data classification and privacy protection policies [US-55-02]
        - IoT device security registry and authentication [US-55-03]
    """,
    'author': 'Jeffery',
    'depends': ['base', 'base_setup', 'farm_core', 'stock', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'views/data_security_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
