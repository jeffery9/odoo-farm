{
    'name': 'Farm Data Security (China)',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'China-specific Data Localization and Cybersecurity Compliance',
    'description': """
        Ensures compliance with China's data localization and cybersecurity regulations [US-18-10].
        - Configuration for data storage region (mainland China).
        - Declaration of Cybersecurity Classified Protection Level 3 compliance.
        - Enhanced audit logging for sensitive operations (e.g., deleting land parcels, exporting farmer info).
    """,
    'author': 'Jeffery',
    'depends': ['base', 'base_setup', 'auditlog'], # 假设有 auditlog 模块
    'data': [
        'security/ir.model.access.csv',
        'views/data_security_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
