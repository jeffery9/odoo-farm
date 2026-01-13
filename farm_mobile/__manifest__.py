{
    'name': 'Farm Mobile',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Mobile Field Operations and Hardware Integration',
    'icon': '/farm_mobile/static/description/icon.svg',
    'description': """
        Mobile capabilities for Odoo 19 Farm System.
        - Hardware Integration: GPS, Camera [US-24-01, US-24-04]
        - Site Check-in and Geofencing Verification [US-24-02]
        - Field Evidence Collection (Photo + GPS) [US-07-05]
        - Automated Timesheet Sync [US-24-03]
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'farm_operation', 'hr_timesheet'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/farm_checkin_views.xml',
        'views/farm_evidence_views.xml',
        'views/farm_mobile_dashboard_views.xml',
        'views/farm_mobile_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'farm_mobile/static/src/js/farm_mobile_checkin.js',
            'farm_mobile/static/src/js/offline_storage.js',
            'farm_mobile/static/src/xml/farm_mobile_checkin.xml',
            'farm_mobile/static/src/scss/farm_mobile.scss',
        ],
    },

    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}