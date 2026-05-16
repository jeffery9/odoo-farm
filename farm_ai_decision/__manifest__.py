{
    "name": "Farm AI Decision Support System",
    "summary": "AI Decision Hub - Stress-Driven Recovery & AI Cockpit Interaction",
    "version": "19.0.1.2.1",
    "category": "Farming",
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "website": "http://www.geninit.cn",
    "maintainers": ["jeffery"],
    "depends": [
        "base",
        "mail",
        "stock",
        "mrp",
        "farm_core",
        "farm_ai_vision",
        "farm_ai_core",
        "farm_agri_science",
        "farm_operation",
        "farm_ai_llm_integration",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/ai_decision_views.xml",
        "views/ai_cockpit_views.xml",
        "views/ai_crop_growth_views.xml",
        "views/ai_pest_decision_views.xml",
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
    "images": ["static/description/main_screenshot.png"],
    "installable": True,
    "application": False,
    "license": "AGPL-3",
    "description": """
[US-202] AI Decision Support Module.
[US-204] AI Decision Cockpit Integration:
- Injects AI recommendation banner into Operation MO views.
- Provides one-tap recovery approval logic.
    """,
}