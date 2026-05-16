{
    'name': 'Agri-Precision',
    'version': '19.0.1.0.0',
    'summary': 'Agricultural specialization for Precision Production (GDD, Nutrients, Agri-Intervention).',
    'category': 'Agriculture',
    'author': 'genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>',
    'website': 'http://www.geninit.cn',
    'depends': ['mrp', 'stock', 'agri_iot', 'farm_operation'],
    'data': [
        'security/ir.model.access.csv',
        'views/precision_bridge_views.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'license': 'AGPL-3',
}
