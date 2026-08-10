{
    'name': 'Farm Mobile',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Mobile Field Operations and Hardware Integration',
    'description': """
        Mobile capabilities for Odoo 19 Farm System.
        - Hardware Integration: GPS, Camera [US-054-01, US-054-04]
        - Site Check-in and Geofencing Verification [US-054-02]
        - Field Evidence Collection (Photo + GPS) [US-007-05]
        - Automated Timesheet Sync [US-054-03]
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'farm_operation', 'hr_timesheet', 'farm_quality', 'farm_iot'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/farm_mobile_dashboard_views.xml',
        'views/farm_mobile_menus.xml',
        'views/farm_checkin_views.xml',
        'views/farm_evidence_views.xml',
        'views/expert_call_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'farm_mobile/static/src/js/farm_mobile_checkin.js',
            'farm_mobile/static/src/js/offline_storage.js',
            'farm_mobile/static/src/xml/farm_mobile_checkin.xml',
            'farm_mobile/static/src/scss/farm_mobile.scss',
        ],
    },

    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}