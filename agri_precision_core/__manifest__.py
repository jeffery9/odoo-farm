{
    'name': 'Agri-Precision Bridge Core',
    'version': '1.0',
    'summary': 'Bridges Odoo Standard Apps with Agriculture & Semiconductor logic (Uncertainty, Grading, Intervention).',
    'category': 'Manufacturing',
    'author': 'genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>',
    'website': 'http://www.geninit.cn',
    'depends': ['mrp', 'stock', 'precision_production', 'agri_iot'],
    'data': [
        'views/precision_bridge_views.xml',
    ],
    'installable': True,
    'license': 'AGPL-3',
}
