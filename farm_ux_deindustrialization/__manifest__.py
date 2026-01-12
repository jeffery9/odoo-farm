{
    'name': 'Farm UX & De-industrialization',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'User Experience & Agricultural Terminology Adaptation',
    'description': """
        User Experience & De-industrialization Module for Odoo 19 Farm Management System.
        
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
        'farm_core', 
        'farm_operation', 
        'farm_marketing', 
        'farm_quality', 
        'farm_safety',
        'base_setup',
        'web'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/term_mapping_views.xml',
        'views/form_layout_template_views.xml',
        'views/visual_status_indicator_views.xml',
        'views/workspace_customization_views.xml',
        'views/contextual_help_views.xml',
        'views/faq_entry_views.xml',
        'views/agricultural_knowledge_views.xml',
        'views/multi_sensory_interaction_views.xml',
        'views/farm_social_network_views.xml',
        'views/accessibility_settings_views.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}