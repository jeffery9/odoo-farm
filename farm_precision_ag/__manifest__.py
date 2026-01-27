{
    'name': 'Farm Precision Agriculture',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Precision Agriculture, VRA and Grid Management',
    'description': """
        Precision Agriculture module for Odoo 19.
        - Spatial Grid Engine (US-46-01)
        - VRA Prescription Engine (US-46-03)
        - NDVI Mapping (US-46-02)
    """,
    'author': 'genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>',
    'website': 'http://www.geninit.cn',
    'depends': ['farm_core'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/precision_ag_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}