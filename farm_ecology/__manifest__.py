{
    'name': 'Farm Ecology & Biodiversity',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Scientific Ecological Data Collection & Biodiversity Tracking',
    'description': """
        Pure ecological data collection and environmental monitoring for sustainable farming [US-17-05].
        - Scientific Biodiversity Indicators (Insects, Birds, Vegetation)
        - Environmental Impact Measurements (pesticide, fertilizer, water, fuel usage)
        - Water Efficiency Data Collection
        - Ecological Infrastructure Monitoring
        NOTE: This module focuses on scientific data collection without ESG governance context.
        ESG assessments and reporting are handled by the farm_esg_* modules.
    """,
    'author': 'Jeffery',
    'depends': ['farm_core', 'farm_sustainability'],
    'data': [
        'security/ir.model.access.csv',
        'views/ecology_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
