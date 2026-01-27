{
    "name": "Farm Biological Asset Valuation",
    "version": "1.0",
    "category": "Industries/Agriculture",
    "summary": "Advanced biological asset valuation with market price integration and fair value accounting",
    "description": """
        Advanced valuation module that provides:
        - Real-time fair value calculation for biological assets
        - Market price integration for commodity pricing
        - Automatic revaluation journal entries
        - Compliance with CAS standards for biological assets
    """,
    "author": "Odoo Farm Dev Team",
    "depends": [
        "farm_core",
        "account",
        "product",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "views/biological_asset_valuation_views.xml",
        "views/market_price_views.xml",
        "views/menu.xml",
    ],
    "installable": True,
    "application": False,
    "license": "AGPL-3",
}