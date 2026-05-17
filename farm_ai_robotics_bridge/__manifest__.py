{
    'name': 'Farm AI - Robotics Bridge',
    'version': '1.0',
    'category': 'Agriculture/AI',
    'summary': 'Bridge module to connect Farm AI Agents with Farm Robotics',
    'depends': ['farm_ai_agent', 'farm_robotics'],
    'data': [
        #'security/ir.model.access.csv',
        'views/mission_log_views.xml'
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'auto_install': True,
    'license': 'AGPL-3',
}
