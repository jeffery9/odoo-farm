{
    "name": "Farm ESG Fair Trade Management",
    "summary": "Manage fair trade certification and community investment aspects of farming ESG",
    "version": "19.0.1.0.0",
    "category": "Farming",
    "author": "genin IT, 亘盈信息技术, jeffery <jeffery9@gmail.com>",
    "maintainers": ["jeffery"],
    "depends": [
        "base",
        "mail",
        "farm_core",
        "farm_hr",
        "farm_esg",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "views/fair_trade_views.xml",
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