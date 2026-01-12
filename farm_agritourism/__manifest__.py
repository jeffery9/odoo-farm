{
    'name': 'Farm Agritourism',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Agritourism, Picking Activities and Plot Adoption',
    'description': """
        Agritourism module for Odoo 19 Farm Management System.
        - Picking & Family Activity Booking [US-02-01]
        - Plot Adoption/Rental Management
        - Integration with Farm Activities
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/farm_booking_views.xml',
        'views/sale_order_views.xml',
    ],
    'demo': [
        'data/farm_agritourism_demo.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}