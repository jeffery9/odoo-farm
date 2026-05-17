{
    "name": "Farm Financial Credit",
    "summary": "Credit scoring and risk assessment for agricultural lending",
    "version": "19.0.1.0.0",
    "category": "Farming",
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "maintainers": ["jeffery"],
    "depends": [
        "base",
        "mail",
        "account",
        "farm_core",
        "farm_financial_core",
        "farm_multi_farm_financial",
    ],
    "data": [
        #"security/ir.model.access.csv",
        "views/credit_scoring_views.xml",
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
    Financial Credit and Risk Assessment Module
    ====================

    This module provides credit scoring and risk assessment capabilities for agricultural lending:
    - Credit scoring models for farmers and agricultural businesses
    - Risk assessment tools for agricultural loans
    - Collateral evaluation for biological assets
    - Credit history tracking
    - Default probability calculations

    Built on top of the farm_financial_core foundation module.
    """,
}