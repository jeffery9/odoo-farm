{
    'name': 'Farm UX',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'User Experience & Agricultural Terminology Adaptation',
    'description': """
        User Experience Module for Odoo 19 Farm Management System.

        Features:
        - Agricultural terminology mapping [US-16-01]
        - Industry-specific form layouts [US-16-02]
        - Visual status indicators [US-16-03]
        - Personalized workspace customization [US-16-04]
        - Smart contextual help [US-16-05]
        - Agricultural knowledge base integration [US-16-06]
        - Multi-sensory interaction experience [US-16-07]
        - Agricultural social & collaboration features [US-16-08]
        - Accessibility & inclusive design [US-16-09]
    """,
    'author': 'Jeffery',
    'depends': [
        'base',
        'web'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/term_mapping_data.xml',
        'data/form_layout_template_data.xml',
        'data/visual_status_indicator_data.xml',
        'data/contextual_help_data.xml',
        'data/multi_sensory_interaction_data.xml',
        'data/accessibility_settings_data.xml',
        'views/menu.xml',
        'views/term_mapping_views.xml',
        'views/form_layout_template_views.xml',
        'views/visual_status_indicator_views.xml',
        'views/workspace_customization_views.xml',
        'views/contextual_help_views.xml',
        'views/multi_sensory_interaction_views.xml',
        'views/farm_social_network_views.xml',
        'views/accessibility_settings_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'farm_ux/static/src/css/workspace_customization.css',
            'farm_ux/static/src/js/farm_ux_integration.esm.js',
            'farm_ux/static/src/js/term_mapping_handler.esm.js',
            'farm_ux/static/src/xml/*.xml',
        ],
    },
    'demo': [
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
    'license': 'AGPL-3',
}