{
    'name': 'Farm Land Management (China)',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'China-specific Land Contract Rights and Land Use Control',
    'description': """
        Implements China's land management regulations [US-041-01].
        - Land Contract Rights Certificate Tracking
        - Land Use Control Validation (e.g., Permanent Basic Farmland protection)
        - Prevents illegal land use for specific agricultural activities.
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'farm_operation', 'farm_agri_science'],
    'data': [
        #'security/ir.model.access.csv',
        'views/land_mgmt_views.xml',
        'views/land_health_rotation_views.xml',
        'views/soil_analysis_views.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
