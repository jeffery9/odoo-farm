{
    "name": "Farm Industry Specialized Layer (ISL)",
    "summary": "Industry Specialized Layer architecture for agricultural operations",
    "version": "19.0.1.0.0",
    "category": "Farming",
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "maintainers": ["jeffery"],
    "depends": [
        "base",
        "mail",
        "stock",
        "mrp",
        "sale",
        "purchase",
        "product",
        "farm_core",
        "farm_quality",
    ],
    "data": [
        #"security/ir.model.access.csv",
        "views/mrp_production_isl_views.xml",
        "views/mrp_bom_isl_views.xml",
        "views/mrp_workcenter_isl_views.xml",
        "views/stock_lot_isl_views.xml",
        "views/sale_order_isl_views.xml",
        "views/purchase_order_isl_views.xml",
        "views/product_template_isl_views.xml",
        "views/stock_picking_isl_views.xml",
        "views/mrp_workorder_isl_views.xml",
        "views/menu.xml",
        
    ],
    "demo": [
    ],
    "images": ["static/description/main_screenshot.png"],
    "installable": True,
    "auto_install": False,
    "license": "AGPL-3",
    "website": "http://www.geninit.cn",
    "description": '''
    ISL (Industry Specialized Layer) Architecture Implementation
    ============

    This module implements the Industry Specialized Layer architecture for agricultural operations,
    allowing for industry-specific specializations while maintaining compatibility with standard Odoo features.

    Documentation:
    - README.md: Core architecture overview
    - INTEGRATION_GUIDE.md: Integration standards for other modules
    - STANDARDIZATION_REPORT.md: Detailed standardization analysis
    - ARCHITECTURE_OVERVIEW.md: Current state and organization patterns
    - INDUSTRY_ISOLATION_GUIDE.md: Industry isolation best practices
    - DATA_ISOLATION_EXAMPLE.py: Sample data migration patterns
    - _INHERITS_IMPLEMENTATION.md: _inherits mechanism best practices
    - _INHERITS_RELATIONSHIP_EXAMPLE.py: _inherits relationship patterns
    - ISL_IMPLEMENTATION_REVIEW.md: Comprehensive implementation review
    - ISL_REVIEW_FINDINGS.md: Key findings and recommendations

    Key Features:
    - Abstract base models for industry specialization
    - Industry-specific extensions for food processing, pharmaceuticals, chemicals
    - Redirection mechanisms from base models to ISL models
    - Performance optimizations
    - Data migration utilities

    The ISL architecture enables agricultural businesses to implement industry-specific requirements
    across different verticals while leveraging shared core functionality.
    ''',
}