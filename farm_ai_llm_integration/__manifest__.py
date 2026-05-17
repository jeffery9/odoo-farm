{
    "name": "Farm LLM Integration Service",
    "summary": "Integration service for Large Language Models in agricultural applications",
    "version": "19.0.1.0.0",
    "category": "Farming",
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "maintainers": ["jeffery"],
    "depends": [
        "base",
        "mail",
        "farm_core",
        "farm_ai"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/llm_config_views.xml",
        "views/llm_service_views.xml",
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
    LLM Integration Service for Agricultural Applications
    ============

    This module provides integration capabilities with Large Language Models (LLMs)
    for agricultural decision support, including OpenAI GPT, Anthropic Claude,
    Google Gemini, and open-source models like Llama.

    Key Features:
    - Configuration management for multiple LLM providers
    - API key management with security
    - Prompt engineering for agricultural domain
    - Integration with existing AI decision modules
    - Caching and rate limiting
    """,
}