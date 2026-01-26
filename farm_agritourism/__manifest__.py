{
    'name': 'Farm Agritourism',
    'version': '1.1',
    'category': 'Industries/Agriculture',
    'summary': 'Agritourism Management - Resource Booking, Activity Management, Membership Services, Experience Project Tracking',
    'description': """
        Agritourism Management Module for Odoo 19 Farm Management System.

        Features:
        - Resource booking and reservation management
        - Activity and experience project management
        - Membership services and loyalty programs
        - Picking & Family Activity Booking [US-02-01]
        - Plot Adoption/Rental Management
        - Integration with Farm Activities
        - Visitor count tracking and management
        - Experience type categorization
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'sale', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'views/farm_booking_views.xml',
        'views/sale_order_views.xml',
        'views/agritourism_operation_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'data/farm_agritourism_demo.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}