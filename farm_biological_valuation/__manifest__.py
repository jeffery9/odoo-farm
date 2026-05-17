{
    "name": "Farm Biological Asset Valuation",
    "summary": "Consolidated biological asset valuation with fair value and cost accounting",
    "version": "19.0.1.0.0",
    "category": "Farming",
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "maintainers": ["jeffery"],
    "depends": [
        "base",
        "mail",
        "account",
        "stock",
        "farm_core",
    ],
    "data": [
        #"security/ir.model.access.csv",
        "views/biological_asset_valuation_views.xml",
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
    Consolidated Biological Asset Valuation Module
    ====================

    This module consolidates biological asset valuation functionality from multiple sources:
    - Fair value accounting with market price integration (from farm_valuation)
    - Cost accounting and depreciation (from farm_finance_advanced)
    - Real-time revaluation with accounting entries
    - Growth stage coefficient management
    - Operational Performance Efficiency (OPE) integration

    Key Features:
    - Fair value and cost-based valuation methods
    - Real-time market price integration
    - Automated revaluation accounting entries
    - Depreciation calculations and entries
    - Growth stage coefficient management
    - Integration with core biological asset model

    The module provides a single, comprehensive solution for biological asset valuation
    while maintaining compatibility with existing systems.
    """,
}