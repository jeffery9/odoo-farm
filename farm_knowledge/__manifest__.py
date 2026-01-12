{
    'name': 'Farm Knowledge Base',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Pest/Disease Identification and Agricultural Knowledge',
    'description': """
        Knowledge management for farmers [US-61].
        - Pest & Disease Database with Photos
        - Solution Recommendations linked to Technical Routes
        - Integration with Field Tasks
    """,
    'author': 'Jeffery',
    'depends': ['farm_planning', 'knowledge'],
    'data': [
        'security/ir.model.access.csv',
        'views/knowledge_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
