{
    'name': 'Farm Agritourism',
    'version': '1.1',
    'category': 'Industries/Agriculture',
    'summary': 'Agritourism Management - Resource Booking, Activity Management, Membership Services, Experience Project Tracking',
    'description': "Agritourism Management Module for Odoo 19 Farm Management System.",
    'author': 'Jeffery',
    'depends': ['farm_core', 'sale', 'project'],
    'data': [
        'views/actions.xml',
        'views/menu.xml',
        'security/ir.model.access.csv',
        'views/farm_booking_views.xml',
        'views/agritourism_operation_views.xml',
    ],
    'demo': [
        'data/farm_agritourism_demo.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}