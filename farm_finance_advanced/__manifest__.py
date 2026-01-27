{
    "name": "Farm Finance Advanced & Specialized Instruments",
    "summary": "Advanced financial instruments and specialized finance for agricultural operations",
    "version": "19.0.1.0.0",
    "category": "Farming",
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "maintainers": ["jeffery"],
    "depends": [
        "base",
        "mail",
        "account",
        "sale",
        "purchase",
        "stock",
        "farm_core",
        "farm_supply",
        "farm_marketing",
        "farm_financial",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/sequence_data.xml",
        "views/livestock_loan_views.xml",
        "views/crop_insurance_views.xml",
        "views/carbon_finance_views.xml",
        "views/futures_hedging_views.xml",
        "views/credit_scoring_views.xml",
        "views/menu.xml",
    ],
    "demo": [
    ],
    "installable": True,
    "auto_install": False,
    "license": "AGPL-3",
    "website": "http://www.geninit.cn",
    "description": """
    Finance Advanced & Specialized Instruments for Agricultural Operations
    ============

    This module implements advanced financial instruments and specialized finance
    solutions for agricultural operations, enabling farmers and agricultural businesses
    to access sophisticated financial tools for risk management and capital optimization.

    Key Features:
    - Live animal asset lending
    - Crop yield insurance
    - Carbon credit financing
    - Agricultural futures and hedging

    The Finance Advanced module provides sophisticated financial instruments tailored
    for the unique needs of modern farming businesses and agricultural risk management.
    """,
}