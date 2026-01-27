{
    'name': 'Farm Smart Greenhouse Control',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Automated Greenhouse Environment and Nutrient Control',
    'description': """
        Smart Greenhouse module for Odoo 19.
        - Environmental Multi-parameter Control [US-57-01]
        - Nutrient Solution & Irrigation Management [US-57-02]
        - Energy Optimization & Carbon Monitoring [US-57-03]
    """,
    'author': 'genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>',
    'website': 'http://www.geninit.cn',
    'depends': ['farm_core', 'farm_iot'],
    'data': [
        'security/ir.model.access.csv',
        'views/farm_greenhouse_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}