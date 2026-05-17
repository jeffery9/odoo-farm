{
    "name": "Farm Financial Core",
    "summary": "Core financial models and utilities for farm management",
    "version": "19.0.1.0.0",
    "category": "Farming",
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "maintainers": ["jeffery"],
    "depends": [
        "base",
        "mail",
        "account",
        "farm_core",
    ],
    "data": [
        #"security/ir.model.access.csv",
    ],
    "demo": [
    ],
    "images": ["static/description/main_screenshot.png"],
    "installable": True,
    "auto_install": False,
    "license": "AGPL-3",
    "website": "http://www.geninit.cn",
    "description": """
    Core Financial Foundation Module
    ====================

    This module provides the core financial models and utilities for the farm management system.
    It serves as the base layer for all financial functionality, providing common models,
    abstract classes, and utilities that specialized financial modules can build upon.

    Key Components:
    - Common financial abstract models
    - Shared financial utilities
    - Base financial models
    - Financial interface definitions

    This module should be installed before any specialized financial modules.
    """,
}