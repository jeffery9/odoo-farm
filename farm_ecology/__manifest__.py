{
    'name': 'Farm Ecology & Biodiversity',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Biodiversity Tracking and Ecological Indicators',
    'description': """
        Ecological management for sustainable farming [US-17-05].
        - Biodiversity Indicators (Insects, Birds, Vegetation)
        - Ecological Infrastructure Maintenance (Hedges, Ponds)
        - ESG Reporting support
    """,
    'author': \"genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>\",
    'depends': ['farm_core', 'farm_sustainability'],
    'data': [
        'security/ir.model.access.csv',
        'views/ecology_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
