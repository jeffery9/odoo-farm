{
    'name': 'Farm Agricultural Robotics',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Agricultural Robotics and Automation Management',
    'description': """
        Robotics module for Odoo 19.
        - Robot Registry and Management [US-61-01]
        - Automated Mission Scheduling [US-61-02]
        - Real-time Operation Monitoring [US-61-03]
    """,
    'author': 'genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>',
    'website': 'http://www.geninit.cn',
    'depends': ['farm_core', 'farm_iot', 'maintenance'],
    'data': [
        'security/ir.model.access.csv',
        'views/farm_robotics_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}