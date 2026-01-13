{
    'name': 'Farm Processing Management',
    'version': '1.1',
    'category': 'Industries/Agriculture',
    'summary': 'Agricultural Product Processing & Transformation',
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
        'farm_ux_deindustrialization'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/processing_data.xml',
        'views/mrp_production_views.xml',
        'views/mrp_bom_views.xml',
        'views/stock_lot_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}