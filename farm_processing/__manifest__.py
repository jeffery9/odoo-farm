{
    'name': 'Farm Processing Management',
    'version': '1.1.1',
    'category': 'Industries/Agriculture',
    'summary': 'Agricultural Product Processing & Transformation',
    'description': """
        Epic 14: Agri-Processing Management.
        
        Features:
        - Primary Processing (Sorting, Cleaning, Packaging) [US-037-01, US-037-08]
        - Deep Processing (Multi-stage BOM, Recipes) [US-037-02, US-037-09]
        - One-in-Multi-out support
        - Full Traceability (Harvest to Final Product) [US-037-03]
        - Mass Balance & Loss Management [US-004-02]
        - Mobile Optimized Kanban Views
        - Energy & Cost Analytic Pivots
    """,
    'author': 'Jeffery',
    'depends': [
        'mrp',
        'mrp_subcontracting',
        'product_expiry',
        'stock',
        'farm_core',
        'farm_mrp',
        'mail',
        'farm_isl',
        'farm_quality'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/processing_data.xml',
        'data/package_data.xml',
        'data/ir_cron_data.xml',
        'views/farm_processing_views.xml',
        'views/menu.xml',
        'views/mrp_production_pivot_view.xml',
        'views/mrp_bom_views.xml',
        'views/mrp_production_views.xml',
        'views/product_views.xml',
        'views/stock_lot_views.xml',
        'views/processing_isl_views.xml',
        'views/recall_wizard_views.xml',
        'views/transformation_wizard_views.xml',
        'views/mrp_workorder_pivot_view.xml',
        'views/package_management_views.xml',
        'views/substitute_wizard_views.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}