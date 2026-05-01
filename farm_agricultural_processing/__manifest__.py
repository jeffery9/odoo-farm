{
    'name': 'Farm Agricultural Processing (Industry Profile)',
    'version': '1.1',
    'category': 'Industries/Agriculture',
    'summary': 'Industry-specific configurations and views for agricultural processing',
    'description': """
        This module provides the industry-specific layer for Agricultural Processing.
        It depends on the core logic provided by 'farm_processing'.

        Features:
        - Industry-specific configuration (Industry Settings)
        - Pre-configured menus for Baking, Winemaking, etc.
        - Simplified views tailored for agri-processing workers.
        - Industry dashboards for Yield and Loss analysis.
    """,
    'author': 'Jeffery',
    'depends': [
        'farm_processing',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/sc_license_views.xml',
        # 'views/mrp_processing_industry_views.xml',
        # 'views/seasonal_bom_views.xml',
        # 'views/mrp_production_views.xml',
        # 'views/mrp_bom_views.xml',
        # 'views/menu.xml',
        # 'views/farm_agricultural_processing_views.xml',
        # 'views/agri_processing_analytics_views.xml',
        # 'views/agri_processing_quality_compliance_views.xml',
        # 'views/agri_processing_net_vegetables_views.xml',
        # 'views/agri_processing_formula_views.xml',
        # 'views/stock_lot_views.xml',
        # 'views/agri_processing_packaging_views.xml',
        # 'views/industry_isl_views.xml',
        # 'views/mrp_production_pivot_view.xml',
    ],
    
    'assets': {
        'web.assets_tests': [
            'farm_agricultural_processing/static/tests/tours/**/*',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}