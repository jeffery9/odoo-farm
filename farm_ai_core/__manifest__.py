{
    "name": "Farm AI Core",
    "summary": "Core AI infrastructure for agricultural applications",
    "version": "19.0.1.0.0",
    "category": "Farming",
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "maintainers": ["jeffery"],
    "depends": [
        "base",
        "mail",
        "farm_core",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/menu.xml",
    ],
    "demo": [],
    "installable": True,
    "auto_install": False,
    "license": "AGPL-3",
    "website": "http://www.geninit.cn",
    "description": """
    AI Core for Agricultural Applications
    ============

    This module provides the core AI infrastructure for agricultural applications,
    including base classes, utilities, and common functionality for all AI modules.

    Key Features:
    - Base AI model classes and mixins
    - Common AI utilities and helpers
    - Configuration management for AI services
    - Model registry and management
    """,
}