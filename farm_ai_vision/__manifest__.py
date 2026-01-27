{
    "name": "Farm AI Vision System",
    "summary": "AI-powered computer vision for agricultural applications",
    "version": "19.0.1.0.0",
    "category": "Farming",
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "maintainers": ["jeffery"],
    "depends": [
        "base",
        "mail",
        "stock",
        "mrp",
        "farm_core",
        "farm_operation",
        "farm_ai_core",
        "farm_quality",
        "farm_livestock",
        "farm_ai_llm_integration"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/ai_vision_base_views.xml",
        "views/ai_pest_disease_views.xml",
        "views/ai_visual_sorting_views.xml",
        "views/ai_image_based_planning_views.xml",
        "views/ai_image_analysis_prediction_views.xml",
        "views/ai_vision_risk_assessment_views.xml",
        "views/menu.xml",
    ],
    "demo": [
    ],
    "installable": True,
    "auto_install": False,
    "license": "AGPL-3",
    "website": "http://www.geninit.cn",
    "description": """
    AI Vision System for Agricultural Applications
    ============

    This module implements AI-powered computer vision for agricultural applications,
    providing image recognition and analysis capabilities to improve farm productivity.

    Key Features:
    - Pest and disease detection from images
    - Visual quality sorting and grading
    - Image-based planting recommendations
    - Image analysis for predictive analytics
    - AI vision risk assessment

    The AI Vision system helps farmers identify problems and opportunities through
    image analysis, enabling data-driven decision making.
    """,
}