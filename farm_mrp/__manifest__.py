{
    'name': 'Farm MRP Base (ISL Infrastructure)',
    'version': '1.1',
    'category': 'Industries/Agriculture',
    'summary': 'Base infrastructure for Industry Specialized Layer (ISL) on MRP models',
    'description': """
        This module provides agricultural-specific extensions and Mixins built on top of
        the general Industry Specialized Layer (ISL) architecture from farm_isl module.

        It adds agriculture-specific functionality, field protection mechanisms,
        and redirection utilities for agricultural verticals (Livestock, Crop, Processing, Aquaculture).

        This module extends the general ISL infrastructure to provide agricultural-specific features.
    """,
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "website": "http://www.geninit.cn",
    'depends': ['mrp', 'stock', 'farm_core', 'farm_isl'],
    'data': [
        'security/ir.model.access.csv',
        'views/mrp_isl_navigation_views.xml',
        'views/stock_matter_tracking_mrp_views.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}