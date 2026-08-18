{
    'name': 'Farm Agricultural Robotics',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Agricultural Robotics and Automation Management',
    'description': """
        Robotics module for Odoo 19.
        - Robot Registry and Management [US-091-01]
        - Automated Mission Scheduling [US-091-02]
        - Real-time Operation Monitoring [US-091-03]
        - Level 5: Robotic A2A Integration [US-100-2026]
    """,
    'author': 'genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>',
    'website': 'http://www.geninit.cn',
    'depends': ['farm_core', 'farm_iot', 'maintenance', 'farm_knowledge', 'project'],
    'data': [
        'data/ir_sequence_data.xml',
        'data/ir_cron_data.xml',
        'security/ir.model.access.csv',
        'views/farm_robotics_views.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}
