{
    'name': 'Farm Processing Management',
    'version': '1.1',
    'category': 'Industries/Agriculture',
    'summary': 'Agricultural product sorting and deep processing',
    'icon': '/farm_processing/static/description/icon.svg',
    'description': """
        Epic 14: Agri-Processing Management.
        
        Features:
        - Primary Processing (Sorting, Cleaning, Packaging) [US-14-01, US-14-08]
        - Deep Processing (Multi-stage BOM, Recipes) [US-14-02, US-14-09]
        - One-in-Multi-out support
        - Full Traceability (Harvest to Final Product) [US-14-03]
        - Mass Balance & Loss Management [US-04-02]
        - Mobile Optimized Kanban Views
        - Energy & Cost Analytic Pivots
    """,
    'author': 'Jeffery',
    'depends': [
        'mrp',
        'stock',
        'farm_core',
        'farm_mrp',
        'farm_ux',
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/processing_data.xml',
        'data/package_data.xml',
        'data/ir_cron_data.xml',
        'views/farm_processing_views.xml',
        'views/mrp_production_pivot_view.xml',
        'views/mrp_bom_views.xml',
        'views/mrp_production_views.xml',
        'views/product_views.xml',
        'views/stock_lot_views.xml',
        'views/processing_isl_views.xml',
        'views/product_isl_views.xml',
        'views/picking_isl_views.xml',
        'views/facility_isl_views.xml',
        'views/menu.xml',
        'views/recall_wizard_views.xml',
        'views/transformation_wizard_views.xml',
        'views/mrp_workorder_pivot_view.xml',
        'views/package_management_views.xml',
        'views/substitute_wizard_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}