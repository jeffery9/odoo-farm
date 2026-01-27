{
    "name": "Farm ESG Environmental Assessment",
    "summary": "ESG environmental assessments using ecological data (from farm_ecology) within ESG governance framework (from farm_esg)",
    "version": "19.0.1.0.0",
    "category": "Farming",
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "maintainers": ["jeffery"],
    "depends": [
        "base",
        "mail",
        "farm_core",
        "farm_esg",
        "farm_ecology",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "views/environmental_views.xml",
        "views/carbon_accounting_views.xml",
        "views/menu.xml",
    ],
    "demo": [
    ],
    "installable": True,
    "auto_install": False,
    "license": "AGPL-3",
    "website": "http://www.geninit.cn"
}