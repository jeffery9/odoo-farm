{
    'name': 'Farm Agricultural Science',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Agricultural Science Research and Experimentation Module',
    'description': """
        Agricultural science module for research and experimentation.
        - Scientific trial management
        - Experimental design and analysis
        - Research data collection
        - Scientific measurements and observations
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'farm_operation'],
    'data': [
        'security/ir.model.access.csv',
        'views/agri_science_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}