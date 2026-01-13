{
    'name': 'Farm Knowledge Base',
    'version': '1.1',
    'category': 'Industries/Agriculture',
    'summary': 'Pest/Disease Identification and Agricultural Knowledge',
    'description': """
        Knowledge management for farmers [US-17-07, US-16-06].
        
        Features:
        - Pest & Disease Database with Photos and Treatment Plans
        - Standard Agricultural Knowledge Articles
        - Best Practice Case Studies
        - Smart Search across all content
        - FAQ Management
        - Mobile-optimized Kanban views
        - Knowledge analytics pivot tables
    """,
    'author': 'Jeffery',
    'depends': ['farm_planning'],
    'data': [
        'security/ir.model.access.csv',
        'views/pest_disease_views.xml',
        'views/agricultural_knowledge_views.xml',
        'views/faq_entry_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}