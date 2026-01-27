{
    "name": "Farm Financial Valuation",
    "summary": "Biological asset valuation and financial instruments",
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
        "farm_financial_core",
        "farm_biological_valuation",  # Using the consolidated module created earlier
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/biological_asset_valuation_views.xml",
        "views/menu.xml",
    ],
    "demo": [
    ],
    "installable": True,
    "auto_install": False,
    "license": "AGPL-3",
    "website": "http://www.geninit.cn",
    "description": """
    Financial Valuation Module
    ====================

    This module provides specialized financial valuation capabilities for farm operations:
    - Biological asset valuation (fair value and cost model)
    - Market price integration for valuation
    - Revaluation accounting entries
    - Growth stage coefficient management

    Built on top of the farm_financial_core foundation module.
    NOTE: This module uses the consolidated farm_biological_valuation module for core valuation functionality.
    """,
}