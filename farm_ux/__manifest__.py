{
    'name': 'Farm UX',
    'version': '1.1.1',
    'category': 'Industries/Agriculture',
    'summary': 'User Experience & Agricultural Terminology Adaptation Framework',
    'description': """
        Base User Experience Framework for Odoo 19 Farm Management System. [US-UX-BASE]
        
        Features:
        - Agricultural terminology mapping [US-039-01]
        - Industry-specific form layouts [US-039-02]
        - Visual status indicators [US-039-03]
        - Multi-sensory interaction experience [US-039-07]
        - Accessibility & inclusive design [US-039-09]
        - Provides Base View Mixins for de-industrialization.
    """,
    'author': 'genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>',
    'website': 'http://www.geninit.cn',
    'depends': [
        'base',
        'web',
        'mrp',
        'stock',
        'farm_core'
    ],
    'data': [
        'views/menu.xml',
        'security/ir.model.access.csv',
        'data/term_mapping_data.xml',
        'data/form_layout_template_data.xml',
        'data/visual_status_indicator_data.xml',
        'data/contextual_help_data.xml',
        'data/multi_sensory_interaction_data.xml',
        'data/accessibility_settings_data.xml',
        'views/term_mapping_views.xml',
        'views/voice_alias_views.xml',
        'views/form_layout_template_views.xml',
        'views/visual_status_indicator_views.xml',
        'views/workspace_customization_views.xml',
        'views/contextual_help_views.xml',
        'views/multi_sensory_interaction_views.xml',
        'views/farm_social_network_views.xml',
        'views/accessibility_settings_views.xml',
        'views/agri_traceability_views.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'farm_ux/static/src/css/workspace_customization.css',
            'farm_ux/static/src/css/accessibility.css',
            'farm_ux/static/src/css/traceability_map.css',
            'farm_ux/static/src/js/farm_ux_integration.esm.js',
            'farm_ux/static/src/js/term_mapping_handler.esm.js',
            'farm_ux/static/src/js/agri_action_buttons.esm.js',
            'farm_ux/static/src/js/agri_dna_integrity.esm.js',
            'farm_ux/static/src/js/agri_gating_audit.esm.js',
            'farm_ux/static/src/js/agri_nutrient_gauge.esm.js',
            'farm_ux/static/src/js/agri_spatial_gauge.esm.js',
            'farm_ux/static/src/js/agri_traceability_map.esm.js',
            'farm_ux/static/src/xml/*.xml',
        ],
    },
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': False,
    'auto_install': True,
    'license': 'AGPL-3',
}
