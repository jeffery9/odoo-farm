{
    "name": "Farm Financial Government Programs",
    "summary": "Government finance and rural revitalization project management",
    "version": "19.0.1.0.0",
    "category": "Farming",
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "maintainers": ["jeffery"],
    "depends": [
        "base",
        "mail",
        "account",
        "farm_core",
        "farm_financial",
        "farm_financial_basic",
    ],
    "data": [
        "security/ir.model.access.csv",
        ],
    "demo": [
    ],
    "images": ["static/description/main_screenshot.png"],
    "installable": True,
    "auto_install": False,
    "license": "AGPL-3",
    "website": "http://www.geninit.cn",
    "description": """
    Financial Government Programs Module
    ====================

    This module provides government-specific financial management:
    - Rural revitalization project funds management
    - Government grant tracking and reporting
    - Special funds accounting and compliance
    - Project-based financial tracking for government programs

    Built on top of the farm_financial foundation module.
    """,
}