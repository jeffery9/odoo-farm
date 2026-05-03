{
    "name": "Farm Financial Basic",
    "summary": "Basic financial management for farm operations",
    "version": "19.0.1.0.0",
    "category": "Farming",
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "maintainers": ["jeffery"],
    "depends": [
        "base",
        "mail",
        "account",
        "analytic",
        "farm_core",
        "farm_operation",
        "farm_financial_core",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/cost_template_views.xml",
        "views/farm_accounting_views.xml",
        "views/menu.xml",
    ],
    "demo": [
    ],
    "images": ["static/description/main_screenshot.png"],
    "installable": True,
    "auto_install": False,
    "license": "AGPL-3",
    "website": "http://www.geninit.cn",
    "description": """
    Basic Financial Management Module
    ====================

    This module provides basic financial management capabilities for farm operations:
    - Cost template management for standard costing
    - Basic accounting integration for farm operations
    - Profitability analysis per production unit
    - Cost tracking and allocation

    Built on top of the farm_financial_core foundation module.
    """,
}