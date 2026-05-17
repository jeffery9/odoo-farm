{
    "name": "Farm ESG Environmental Assessment",
    "summary": "ESG environmental assessments using ecological data (from farm_ecology) within ESG governance framework (from farm_esg) - VRA Environmental Impact Assessment (Epic 80)",
    "version": "19.0.1.0.0",
    "category": "Farming",
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "maintainers": ["jeffery"],
    "description": """
ESG Environmental Assessment module for Odoo 19 Farm Management System - Epic 80 Implementation.
- VRA carbon footprint calculation and reduction analysis
- Water body protection VRA strategies with buffer zones
- Soil health VRA models with health metrics integration
- Environmental risk assessment and compliance
- Integration with ESG governance framework for comprehensive sustainability tracking
    """,
    "depends": [
        "base",
        "mail",
        "farm_core",
        "farm_esg",
        "farm_ecology",
        "farm_agri_science",
        "farm_operation",  # For interventions
        "farm_iot",  # For sensor data
        "farm_equipment", # For fuel logs to carbon ledger
    ],
    "data": [
        #"security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "views/environmental_views.xml",
        "views/carbon_accounting_views.xml",
        "views/esg_red_line_monitoring_views.xml",
        "views/vra_carbon_footprint_views.xml",
        "views/vra_water_protection_views.xml",
        "views/vra_soil_health_views.xml",
        "views/menu.xml",
    ],
    "demo": [
    ],
    "images": ["static/description/main_screenshot.png"],
    "installable": True,
    "auto_install": False,
    "license": "AGPL-3",
    "website": "http://www.geninit.cn"
}