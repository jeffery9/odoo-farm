{
    'name': 'Farm Agritourism',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Agritourism, Picking Activities and Plot Adoption',
    'description': """
        Agritourism module for Odoo 19 Farm Management System.
        - Picking & Family Activity Booking [US-51]
        - Plot Adoption/Rental Management
        - Integration with Farm Activities
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/farm_booking_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
