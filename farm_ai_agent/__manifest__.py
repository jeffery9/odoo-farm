{
    "name": "Farm AI Agent System",
    "summary": "AI agent framework for orchestrating agricultural AI services",
    "version": "19.0.1.0.0",
    "category": "Farming",
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "maintainers": ["jeffery"],
    "depends": [
        "base",
        "mail",
        "farm_core",
        "farm_ai",
        "farm_ai_vision",
        "farm_ai_decision",
        "farm_financial_insurance",
        "farm_ai_llm_integration",
        "farm_agri_science"
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/security_rules.xml",
        "data/ir_sequence_data.xml",
        "data/ir_cron_data.xml",
        "views/a2a_react_loop_views.xml",
        "views/ai_skill_views.xml",
        "views/menu.xml",
        "views/ai_agent_views.xml",
        "views/ai_decision_engine_views.xml",
        "views/mission_orchestrator_views.xml",
        "views/digital_twin_cockpit_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "farm_ai_agent/static/src/css/digital_twin_cockpit.css",
            "farm_ai_agent/static/src/js/digital_twin_cockpit.js",
            "farm_ai_agent/static/src/xml/digital_twin_cockpit.xml"
        ]
    },
    "demo": [
    ],
    "images": ["static/description/main_screenshot.png"],
    "installable": True,
    "auto_install": False,
    "license": "AGPL-3",
    "website": "http://www.geninit.cn",
    "description": """
    AI Agent System for Agricultural Applications
    ============

    This module implements an AI agent framework for orchestrating agricultural AI services.

    Key Features:
    - Unified AI agent framework for orchestrating different AI services
    - Centralized decision engine coordinating between different AI models
    - L5 Autonomous Mission Orchestrator: Auto-dispatches robot clusters based on biological twin alerts
    - Integration of vision, decision, and LLM AI services
    - Enhanced LLM integration for domain-specific intelligence
    """,
}