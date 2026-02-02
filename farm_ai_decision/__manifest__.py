{
    "name": "Farm AI Decision Support System",
    "summary": "AI Decision Hub - Stress-Driven Recovery & Dynamic Harvest Prediction",
    "version": "19.0.1.1.0",
    "category": "Farming",
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "website": "http://www.geninit.cn",
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
        "farm_agri_science",
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
    "installable": True,
    "application": False,
    "license": "AGPL-3",
    "description": """
[US-202] AI Decision Support Module.
1. Active Recovery Decisions based on Biological Stress Index.
2. Dynamic Harvest Window Prediction using Physiological Age (GDD).
3. Integrated Active Skill JSON Instruction Dispatch.

Legacy Features Preserved:
- Crop growth prediction and recommendations
- Pest and disease identification with solutions
- Smart irrigation and fertilization decisions
- Market price prediction and sales strategy
    """,
}