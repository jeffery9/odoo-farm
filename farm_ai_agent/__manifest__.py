{
    "name": "Farm AI Decision System",
    "summary": "Unified AI-driven agricultural intelligent decision support system",
    "version": "19.0.1.0.0",
    "category": "Farming",
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "maintainers": ["jeffery"],
    "depends": [
        "base",
        "mail",
        "farm_core",
        "farm_operation",
        "farm_ai_vision",
        "farm_ai_decision",
        "farm_ai_llm_integration",
        "farm_finance_advanced",
        "farm_isl",
        "farm_robotics",
        "farm_agri_science"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/ai_agent_views.xml",
        "views/ai_decision_engine_views.xml",
        "views/mission_orchestrator_views.xml",
        "views/menu.xml",
    ],
    "demo": [
    ],
    "installable": True,
    "auto_install": False,
    "license": "AGPL-3",
    "website": "http://www.geninit.cn",
    "description": """
    AI Decision System for Agricultural Applications
    ============

    This module implements a unified AI-driven agricultural intelligent decision support system.

    Key Features:
    - Unified AI agent framework for orchestrating different AI services
    - Centralized decision engine coordinating between different AI models
    - L5 Autonomous Mission Orchestrator: Auto-dispatches robot clusters based on biological twin alerts
    - Integration of vision, decision, and financial AI services
    - Enhanced LLM integration for domain-specific intelligence
    """,
}