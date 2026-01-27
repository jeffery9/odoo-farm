{
    "name": "Farm AI Decision Support System",
    "summary": "AI-powered decision support for agricultural operations",
    "version": "19.0.1.0.0",
    "category": "Farming",
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "maintainers": ["jeffery"],
    "depends": [
        "base",
        "mail",
        "stock",
        "mrp",
        "sale",
        "purchase",
        "product",
        "farm_core",
        "farm_operation",
        "farm_supply",
        "farm_ecology",
        "farm_ai_core",
        "farm_ai_llm_integration",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/ai_decision_views.xml",
        "views/ai_crop_growth_views.xml",
        "views/ai_pest_detection_views.xml",
        "views/ai_irrigation_views.xml",
        "views/ai_fertilization_views.xml",
        "views/ai_market_prediction_views.xml",
        "views/ai_harvest_views.xml",
        "views/ai_path_optimization_views.xml",
        "views/ai_resource_optimization_views.xml",
        "views/ai_quality_grading_views.xml",
        "views/ai_disease_monitoring_views.xml",
        "views/ai_risk_assessment_views.xml",
        "views/ai_agent_views.xml",
        "views/menu.xml",
    ],
    "demo": [
    ],
    "installable": True,
    "auto_install": False,
    "license": "AGPL-3",
    "website": "http://www.geninit.cn",
    "description": """
    AI Decision Support System for Agricultural Operations
    ============

    This module implements AI-powered decision support for agricultural operations,
    providing intelligent recommendations and predictive analytics to improve farm productivity.

    Key Features:
    - Crop growth prediction and recommendations
    - Pest and disease identification with solutions
    - Smart irrigation and fertilization decisions
    - Market price prediction and sales strategy
    - Harvest timing optimization
    - Resource allocation optimization
    - Quality grading automation
    - Health and welfare monitoring
    - Risk assessment and insurance recommendations
    - Knowledge management and technology recommendations

    The AI Decision Support system helps farmers make data-driven decisions to optimize
    productivity, reduce costs, and improve sustainability.
    """,
}